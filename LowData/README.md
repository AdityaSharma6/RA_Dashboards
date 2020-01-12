# BigDataDashboard

DEPLOYING STEPS:
heroku login
git status
git add .
git commit -m "MESSAGE"
heroku create -n "NAME"
heroku git:remote -a "NAME"
git push heroku master
heroku ps:scale web=1