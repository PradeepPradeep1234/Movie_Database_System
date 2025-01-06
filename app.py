from flask import Flask,render_template,request,redirect

app = Flask(__name__)

tasks=[]
@app.route('/',methods=["POST","GET"])
def main():
    if request.method == "POST":
        my_task = request.form["task"]
        tasks.append(my_task)
        return redirect('/')

    return render_template('index.html',tasks=tasks)

@app.route('/delete',methods=["POST"])
def delete():

    del_task = request.form["task"]
    if del_task in tasks:
        tasks.remove(del_task)
    return redirect('/')


    

if __name__ == '__main__':
    app.run( debug=True)
