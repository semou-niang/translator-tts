"""Configuration et fixtures communes pour pytest (strictement hors ligne)."""

import socket

import pytest


@pytest.fixture(autouse=True)
def deny_network(monkeypatch):
    original_connect = socket.socket.connect

    def connect(sock, address):
        # asyncio Windows crée son canal interne par socketpair TCP en loopback.
        if isinstance(address, tuple) and address[0] in ("127.0.0.1", "::1"):
            return original_connect(sock, address)
        raise AssertionError("Réseau externe interdit dans les tests hors ligne.")

    def fail(*args, **kwargs):
        raise AssertionError("Réseau interdit dans les tests hors ligne.")

    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket, "create_connection", fail)
