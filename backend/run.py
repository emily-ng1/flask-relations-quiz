from api import create_app

app = create_app('adventureworks')
app.run(debug = True)