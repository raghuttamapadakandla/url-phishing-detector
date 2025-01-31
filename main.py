from flask import Flask, render_template, request, redirect, session
import check_phish
import time

app = Flask(__name__)
app.secret_key = b'\xeb\xa2\xc9\x1b#\x84\xb8\x1cjq\xc0\x1e3\x11+\xc9'

DEFAULT_SESSION = {
    'value_check': False,
    'domain': '',
    'verdict': '',
    'job_id': '',
    'raw_response': {'scan': {}, 'status': {}}
}

MAX_RETRIES = 30  # 30 seconds maximum wait
CHECK_INTERVAL = 1  # Check every 1 second

@app.route('/', methods=['GET'])
def render_home():
    session.update(DEFAULT_SESSION)
    return render_template('home.html')

@app.route('/', methods=['POST'])
def get_domain():
    session.update(DEFAULT_SESSION)
    domain = request.form.get('Domain')
    if domain:
        session['domain'] = domain
        session['value_check'] = True
    return redirect('/check')

@app.route('/check')
def check_domain():
    if not session.get('value_check'):
        return redirect('/')
    
    try:
        # Submit initial scan
        scan_response = check_phish.submit_scan(session['domain'], 'quick')
        session['raw_response']['scan'] = scan_response
        job_id = scan_response.get('jobID')
        
        if not job_id:
            raise ValueError("No jobID in scan response")

        # Continuously check status until done
        retries = 0
        scan_result = None
        
        while retries < MAX_RETRIES:
            scan_result = check_phish.check_scan_status(job_id, True)
            current_status = scan_result.get('status', '').upper()
            
            if current_status == 'DONE':
                break
                
            retries += 1
            time.sleep(CHECK_INTERVAL)
        else:
            # Timeout occurred
            session['verdict'] = 'timeout'
            session['value_check'] = False
            return render_template('timeout.html')

        # Store final results
        session['raw_response']['status'] = scan_result
        verdict = scan_result.get('disposition', 'unknown')
        session['verdict'] = verdict

    except Exception as e:
        print(f"Error: {str(e)}")
        session['verdict'] = 'error'
    
    session['value_check'] = False
    return redirect('/results')

@app.route('/results')
def result_page_render():
    verdict = session.get('verdict', 'error')
    
    # Reset session first
    session.update(DEFAULT_SESSION)
    
    # Render appropriate template
    if verdict == 'clean':
        return render_template('legitimate.html')
    elif verdict == 'phish':
        return render_template('phishing.html')
    elif verdict == 'timeout':
        return render_template('timeout.html')
    else:
        return render_template('error.html')
    
    # verdict = session.get('verdict', 'error'),
    # retries_used = min(MAX_RETRIES, len(session['raw_response'].get('status_checks', [])))

    # if verdict == 'clean':
    #     response = render_template('legitimate.html')
    # else:
    #     response = render_template('phishing.html')
   
    # session.update(DEFAULT_SESSION)
    # return response

# if __name__ == '__main__':
#     app.run()