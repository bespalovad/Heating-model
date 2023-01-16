from flask import Flask, render_template, url_for, request
import psycopg2
import psycopg2.extras
from youtube import get_views

DB_name='YouTube'
DB_host='localhost'
DB_port='5432'
DB_user='postgres'
DB_password='5555'

app = Flask(__name__)

stop_list = ['убийство', 'вбивство', 'murder', 'war', 'война', 'війна', 'наркотики', 'drugs', 'blood', 'кров', 'кровь', 'расстрел', 'розстріл', 'execution', 'казнь', 'страта']

requests = ["", "", ""]

data = [["", "", ""], ["", "", ""], ["", "", ""]]

message = ""

def word_check (word):
	if (word in stop_list) | (len(word) > 100) | (word == ""):
		return 0
	return 1

def connect_to_DB():
    try:
        print("done")
        return psycopg2.connect(dbname=DB_name, user=DB_user, password=DB_password, host=DB_host, port=DB_port)
    except:
        print('Failed Connection')

conn=connect_to_DB()

@app.route('/')
def index():
	return (render_template("index.html", message=message))
	
@app.route('/results', methods=['GET', 'POST'])
def results():
	global requests
	global data
	global message
	if request.method == 'POST':
		message = ""
		try:
			d = int(request.form["deleted"])
			requests.pop(d)
			data.pop(d)
			requests.append("")
			data.append(["", "", ""])
			return (render_template("analysis.html", requests=requests, message=message, data=data))
		except (Exception, psycopg2.Error) as error:
			print("Failed to insert record into mobile table", error)
		
		req = request.form["joke"]
		print(word_check(req))
		if word_check(req):
			try:
				match (request.form["submit_button"]):
					case "Prognosis":
						try:
							#conn = connect_to_DB()
							#cur = conn.cursor()
						
							# data base connection etc.
							requests[0] = req
							requests[1] = ""
							requests[2] = ""
							
							a, b, c = get_views(req)#Розрахунок прогнозу (data)
							data[0] = ["Середня кількість переглядів: " + str(a), "Середній час публікації (у роках): " + str(b), "Середня довжина відео (у хвилинах): " + str(c)]
							data[1] = ["", "", ""]
							data[2] = ["", "", ""]
							
							return (render_template("prognosis.html", requests=requests, data='Прогнозована кількість переглядів за рік: {:.3f}'.format((10*a)/(b*c)), message=message))
						
						except (Exception, psycopg2.Error) as error:
							print("Failed to insert record into mobile table", error)

						finally:
							if 0:
								cur.close()
								print("PostgreSQL connection is closed")
							
					case "Analysis":
						try:
							#conn = connect_to_DB()
							#cur=conn.cursor()
						
							# data base connection etc.
							new = 1
							for i in requests:
								if req == i:
									new = 0
							print ("s1")
							if new:
								if requests[0] == "":
									requests[0] = req
									data[0] = list(get_views(req))
									data[0][0] = "Середня кількість переглядів: " + str(data[0][0])
									data[0][1] = "Середній час публікації (у роках): " + str(data[0][1])
									data[0][2] = "Середня довжина відео (у хвилинах): " + str(data[0][2])
									print ("s2")
								elif requests[1] == "":
									requests[1] = req
									data[1] = list(get_views(req))
									data[1][0] = "Середня кількість переглядів: " + str(data[1][0])
									data[1][1] = "Середній час публікації (у роках): " + str(data[1][1])
									data[1][2] = "Середня довжина відео (у хвилинах): " + str(data[1][2])
									print ("s3")
								elif requests[2] == "":
									requests[2] = req
									data[2] = list(get_views(req))
									data[2][0] = "Середня кількість переглядів: " + str(data[2][0])
									data[2][1] = "Середній час публікації (у роках): " + str(data[2][1])
									data[2][2] = "Середня довжина відео (у хвилинах): " + str(data[2][2])
									print ("s4")
								else: message = "Only three requests allowed"
							else: message = "This request is already shown" 
							
							#Розрахунок аналітики
						
							return (render_template("analysis.html", requests=requests, message=message, data=data))
						
						except (Exception, psycopg2.Error) as error:
							print("Failed to insert record into mobile table", error)
							return render_template('index.html',message='Something went wrong. Try again')

						finally:
							conn = 0
							if conn:
								cur.close()
								print("PostgreSQL connection is closed")
								
					case _:
						return (render_template("index.html", message=message))
			except (Exception, psycopg2.Error) as error:
				print("Failed to insert record into mobile table", error)
		else:
			message = "Restricted request."
			try:
				match (request.form["submit_button"]):
					case "Prognosis":
						requests = ["", "", ""]
						data = [["", "", ""], ["", "", ""], ["", "", ""]]
						message = "Порожній запит"
						return (render_template("prognosis.html", requests=["Немає запиту", "", ""], data="Немає даних", message=message))
					case "Analysis":
						return (render_template("analysis.html", requests=requests, message=message, data=data))
					case _:
						return (render_template("index.html", message=message))
			except (Exception, psycopg2.Error) as error:
				print("Failed to insert record into mobile table", error)
					
				
	'''if request.method == 'GET':
		match (request.form["submit_button"]):
			case "Prognosis":
				try:
					#conn = connect_to_DB()
					#cur=conn.cursor()
				
					# data base connection etc.

					
				
				except (Exception, psycopg2.Error) as error:
					print("Failed to insert record into mobile table", error)

				finally:
					conn = 0
					if conn:
						cur.close()
						print("PostgreSQL connection is closed")
					
			case "Analysis":
				try:
					#conn = connect_to_DB()
					#cur=conn.cursor()
				
					# data base connection etc.
					
					
				
				except (Exception, psycopg2.Error) as error:
					print("Failed to insert record into mobile table", error)

				finally:
					conn = 0
					if conn:
						cur.close()
						print("PostgreSQL connection is closed")
						
			case _:
				conn = 0'''


def main(args):
	return 0

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=int(8000), debug=True)
