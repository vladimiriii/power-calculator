# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, redirect, url_for, request, Response
import os
import sys

from app.lib import testMap
from app.lib import textInserts as txt

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


@test_page.route('/tests/<test_type>', methods=['GET'])
def test_page_renderer(test_type):
    text = txt.generate_fixed_text(test_type)
    return render_template('test-page.html', text=text)


@api_endpoint.route('/tests/<test_type>-calc', methods=['POST'])
def test_page_data(test_type):
    try:
        input = json.loads(request.data)
        f = testMap.map[test_type]
        results = f.handler.run_model(input)
        return jsonify(results)
    except Exception as e:
        return Response("{'error': '" + str(e) + "'}", status=400, mimetype='application/json')
