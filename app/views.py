# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, redirect, url_for, request
import os
import sys

from app.lib import t_test


# Define the blueprint:
basic_page = Blueprint('basic_page', __name__)
test_page = Blueprint('test_page', __name__)
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


@test_page.route('/t-test-two-independent-samples', methods=['GET'])
def t_test_two_ind():
    return render_template('t-test-two-ind.html')


@api_endpoint.route('/t-test-2-sample-ind-calc', methods=['POST'])
def t_test_ind():
    input = json.loads(request.data)
    results = t_test.calculate_statistics(input)
    return jsonify(results)
