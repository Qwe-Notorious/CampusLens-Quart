from CampusLens.route import app, csfr

if __name__ == "__main__":
    app.run(debug=True)
    csfr.init_app(app)
