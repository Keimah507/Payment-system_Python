from src.app.app import app

@app.route('/deposit', methods = ['GET', 'POST'])
def deposit():
    """
    Deposits fund into wallet
    """
    form = DepositForm()
    if form.validate_on_submit():
        amount = form.amount.data
        user = current_user
        user.deposit(amount)
        stripe.api_key = os.environ.get('Stripe Secret Key')
        charge = stripe.Charge.Create(
            amount=int(amount*100),
            currency = 'usd',
            descripiton = 'deposit into custom app wallet',
            source=request.form['stripeToken']
        )
        flash('Funds deposited succesfully!', 'success')
        return redirecturl(url_for('dashboard'))
    return render_template('deposit.html', form=form)