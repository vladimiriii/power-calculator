# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, redirect, url_for, request, Response
import os
import sys

from app.lib import statistics
from app.lib import charts
from app.lib import formulae

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
    try:
        input = json.loads(request.data)
        stats_data = statistics.t_test.calculate_statistics(input)
        chart_data = charts.t_test.generate_chart_data(input, stats_data)
        formulas_and_notes = formulae.t_test.generate_formulas(input)
        return jsonify({
            "statistics": stats_data,
            **formulas_and_notes,
            **chart_data
        })
    except Exception as e:
        return Response("{'error': '" + str(e) + "'}", status=400, mimetype='application/json')
