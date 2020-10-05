# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, redirect, url_for, request
import os
import sys

from app.lib import t_test_methods as ttest


# Define the blueprint:
basic_page = Blueprint('basic_page', __name__)
api_endpoint = Blueprint('api_endpoint', __name__)


@basic_page.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')


@basic_page.route('/terms-conditions', methods=['GET'])
def terms_conditions_page():
    return render_template('terms-conditions.html')


@basic_page.route('/privacy-policy', methods=['GET'])
def privacy_policy_page():
    return render_template('privacy-policy.html')


@api_endpoint.route('/t-test-ind', methods=['GET'])
def t_test_ind():
    array = {"foo": "foo"}
    return jsonify(array)
