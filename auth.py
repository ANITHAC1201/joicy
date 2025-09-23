import os
import sqlite3
import hashlib
import secrets
from datetime import datetime
import streamlit as st
from typing import Optional, Tuple, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


# Password hashing utilities (PBKDF2-HMAC with SHA256)
ITERATIONS = 200_000


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), bytes.fromhex(salt), ITERATIONS
    ).hex()
    return salt, pwd_hash


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    _, pwd_hash = hash_password(password, salt)
    return secrets.compare_digest(pwd_hash, expected_hash)


# User operations

def user_exists(username: str, email: str) -> Tuple[bool, Optional[str]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, email FROM users WHERE username = ? OR email = ?", (username, email))
    row = cur.fetchone()
    conn.close()
    if row:
        if row[0] == username:
            return True, 'username'
        if row[1] == email:
            return True, 'email'
    return False, None


def register_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    exists, field = user_exists(username, email)
    if exists:
        if field == 'username':
            return False, 'Username already taken'
        if field == 'email':
            return False, 'Email already registered'
    salt, pwd_hash = hash_password(password)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, email, pwd_hash, salt, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    return True, 'Registration successful'


def authenticate_user(username_or_email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, password_hash, salt FROM users WHERE username = ? OR email = ?",
        (username_or_email, username_or_email),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return False, 'User not found', None
    user = {
        'id': row[0],
        'username': row[1],
        'email': row[2],
        'password_hash': row[3],
        'salt': row[4],
    }
    if verify_password(password, user['salt'], user['password_hash']):
        return True, 'Authenticated', user
    return False, 'Invalid credentials', None


# Streamlit helpers

def require_login():
    if not st.session_state.get('authenticated'):
        st.info("Please log in from the 'Login' page in the sidebar.")
        st.stop()


def login_user_session(user: Dict):
    st.session_state['authenticated'] = True
    st.session_state['user'] = {'id': user['id'], 'username': user['username'], 'email': user['email']}


def logout_user_session():
    for key in ['authenticated', 'user']:
        if key in st.session_state:
            del st.session_state[key]


def current_user() -> Optional[Dict]:
    return st.session_state.get('user')


# Initialize DB on import
init_db()
