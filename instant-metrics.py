#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest
import os
import re

app = Flask(__name__)

registry = CollectorRegistry()
cpu_instant_gauge = Gauge('cpu_instant', 'cpu instant value', ['mode'], registry=registry)

@app.route('/metrics')
def metrics():
	metrics = ['-1','-1','-1','-1','-1','-1','-1','-1']
	try:
		line=os.popen("sar -u 1 1").readlines()[3].strip()
		metrics = re.split(' +',line)
	except BaseException, e:
		print(e.args)
	finally:
		cpu_instant_gauge.labels("user").set(metrics[2])
		cpu_instant_gauge.labels("nice").set(metrics[3])
		cpu_instant_gauge.labels("system").set(metrics[4])
		cpu_instant_gauge.labels("iowait").set(metrics[5])
		cpu_instant_gauge.labels("steal").set(metrics[6])
		cpu_instant_gauge.labels("idle").set(metrics[7])
		return Response(generate_latest(cpu_instant_gauge), mimetype='text/plain')





if __name__ == '__main__':
	from waitress import serve
	serve(app, host='0.0.0.0', port=5000)
