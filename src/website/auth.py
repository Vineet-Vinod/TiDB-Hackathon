from flask import Blueprint, render_template, request, flash, redirect, url_for
from email_validator import validate_email, EmailNotValidError
import re

auth = Blueprint("auth", __name__)