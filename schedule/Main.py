from tkinter import*
from tkinter import ttk

class turn():
	def __init__(self, start, finish):
		self.start=start
		self.finish=finish
class process(object):
	"""docstring for process"""
	
	def __init__():
		pass
	
	def __init__(self,name, arrival_time, burst_time, priority=-1):
		self.name=name;
		self.arrival_time=arrival_time;
		self.burst_time=burst_time;
		self.priority=priority;
		self.turns=[]
		self.done=0;
		self.waiting_time=0
		self.turnaround=0

	def init(self, name, arrival_time, burst_time, priority=-1):
		self.name=name;
		self.arrival_time=arrival_time;
		self.burst_time=burst_time;
		self.priority=priority;
		self.turns=[]
		self.done=0;
'''
def test(p_list):
	for p in p_list:
		for t in p.turns:
			print (t.start," ",p.name ," ", t.finish,"-> " , end='',flush=TRUE)

'''

def sort_by(attr,p_list):
	if(attr=="name"):
		for i in range(0,len(p_list)-1):
			for j in range(0,len(p_list)-1-i):
				if(p_list[j].name>p_list[j+1].name):
					p_list[j],p_list[j+1]=p_list[j+1],p_list[j]

	if(attr=="burst_time"):
		for i in range(0,len(p_list)-1):
			for j in range(0,len(p_list)-1-i):
				if(p_list[j].burst_time>p_list[j+1].burst_time):
					p_list[j],p_list[j+1]=p_list[j+1],p_list[j]

	if(attr=="priority"):
		for i in range(0,len(p_list)-1):
			for j in range(0,len(p_list)-1-i):
				if(p_list[j].priority>p_list[j+1].priority):
					p_list[j],p_list[j+1]=p_list[j+1],p_list[j]

	if(attr=="arrival_time"):
		for i in range(0,len(p_list)-1):
			for j in range(0,len(p_list)-1-i):
				if(p_list[j].arrival_time>p_list[j+1].arrival_time):
					p_list[j],p_list[j+1]=p_list[j+1],p_list[j]
def priority_P_calc(p_list,len,begin,end):
	min_pri_process=p_list[0]
	for i in range(len):
		if(p_list[i].priority<min_pri_process.priority):
			min_pri_process=p_list[i]

def calc_Turnaround_waiting_time(p_list,backup_l,result):
	sort_by("name",p_list)
	sort_by("name",backup_l)
	avg_waiting=0
	avg_turnaround=0
	for ii in range(len(p_list)):
		p_list[ii].turnaround=p_list[ii].turns[len(p_list[ii].turns)-1].finish-backup_l[ii].arrival_time
		avg_turnaround=avg_turnaround+p_list[ii].turnaround
	for ii in range(len(p_list)):
		for i in range(len(p_list[ii].turns)-1):
			p_list[ii].waiting_time=p_list[ii].waiting_time+(p_list[ii].turns[i+1].start-p_list[ii].turns[i].finish)
		p_list[ii].waiting_time=p_list[ii].waiting_time+(p_list[ii].turns[0].start-p_list[ii].arrival_time)
		avg_waiting=avg_waiting+p_list[ii].waiting_time
	avg_waiting=avg_waiting/len(backup_l)
	avg_turnaround=avg_turnaround/len(backup_l)
	result.append(avg_waiting)
	result.append(avg_turnaround)
def schedule():
	try:
		backup=[]
		processes=[]
		for e in range(len(Entry_list)):
			if(Entry_variables[e][1].get()<=0):
				print('\007')
				return
			if(Entry_variables[e][0].get()<0):
				print('\007')
				return
			x=Entry_variables[e][0].get()
			y=Entry_variables[e][1].get()
			if(combobox.get()!='Priority (Preemptive)' and combobox.get()!='Priority (Non Preemptive)'):
				z=0
			else:	
				z=Entry_variables[e][2].get()
			if(z<0):
				print('\007')
				return	
			p=process('P'+str(e+1),x,y,z)
			processes.append(p)
		
		schuduling_type=combobox.get()
		quant_time=quantum_var.get()
		if(schuduling_type=='Round Robin' and quant_time<=0):
			print('\007')
			return

		for p in processes:
			temp_p=process(p.name,p.arrival_time,p.burst_time,p.priority)
			backup.append(temp_p)

		


		if(schuduling_type=="FCFS"):
			now=0
			sort_by("arrival_time",processes);
			for i in processes:
				start=now
				if(now<i.arrival_time):
					start=i.arrival_time
				temp_turn=turn(start,start+i.burst_time)
				i.turns.append(temp_turn)
				now=start+i.burst_time
				#print(i.arrival_time," ",i.burst_time)

		elif(schuduling_type=="SJF (Non Preemptive)"):	
			now=0
			finished=0;
			while  finished<len(processes):
				sort_by("burst_time",processes)
				flag=0
				for p in processes:
					start=now
					if(p.arrival_time<=now and p.done==0):
						if(now<p.arrival_time):
							start=p.arrival_time
						temp_turn=turn(start,start+p.burst_time)
						p.turns.append(temp_turn)
						now=now+p.burst_time
						p.done=1
						finished=finished+1
						flag=1
						break
				if(flag==0):
					sort_by("arrival_time",processes)
					for p in processes:
						if(p.done==0):
							now=p.arrival_time;
							break
		elif(schuduling_type=="SJF (Preemptive)"):
			ready=[]
			running=[]
			i=0
			sort_by("burst_time",processes)
			sort_by("arrival_time",processes)
			while(i<len(processes)):
				now=processes[i].arrival_time
				if(i==0):
					running.append(processes[i])
					start=now
					#processes.pop(i)
				else:
					if(running[0].burst_time+start<=now):
						temp_turn=turn(start,start+running[0].burst_time)
						now=running[0].burst_time+start
						running[0].turns.append(temp_turn)
						running[0].done=1
						running[0].burst_time=0
						running.pop()
						if(len(ready)>0):
							running.append(ready[0])
							ready.pop(0)
							start=now
							i=i-1

						else:
							now=processes[i].arrival_time
							running.append(processes[i])
							start=now
							
					else:
						if(processes[i].burst_time<(running[0].burst_time-(now-start))):
							temp_turn=turn(start,now)
							running[0].turns.append(temp_turn)
							running[0].burst_time=running[0].burst_time-(now-start)
							ready.append(running[0])
							sort_by("burst_time",ready)
							running.pop()
							running.append(processes[i])
							start=now
						else:
							ready.append(processes[i])
							sort_by("burst_time",ready)
				i=i+1
			    
				
			if(len(running)>0 and running[0].burst_time!=0):
				now=start+running[0].burst_time
				temp_turn=turn(start,now)
				running[0].turns.append(temp_turn)	
				running[0].burst_time=0
				running[0].done=1
				running.pop()

			while(len(ready)>0):
				running.append(ready[0])
				ready.pop(0)
				start=now
				now=start+running[0].burst_time
				temp_turn=turn(start,now)
				running[0].turns.append(temp_turn)	
				running[0].burst_time=0
				running[0].done=1
				running.pop()
				


			if(len(running)>0 and running[0].burst_time!=0):
				now=start+running[0].burst_time
				temp_turn=turn(start,now)
				running[0].turns.append(temp_turn)	
				running[0].burst_time=0
				running[0].done=1
				running.pop()	
					

		elif(schuduling_type=="Priority (Preemptive)"):
			ready=[]
			running=[]
			i=0
			sort_by("priority",processes)
			sort_by("arrival_time",processes)
			while(i<len(processes)):
				now=processes[i].arrival_time
				if(i==0):
					running.append(processes[i])
					start=now
					#processes.pop(i)
				else:
					if(running[0].burst_time+start<=now):
						temp_turn=turn(start,start+running[0].burst_time)
						now=running[0].burst_time+start
						running[0].turns.append(temp_turn)
						running[0].done=1
						running[0].burst_time=0
						running.pop()
						if(len(ready)>0):
							running.append(ready[0])
							ready.pop(0)
							start=now
							i=i-1

						else:
							now=processes[i].arrival_time
							running.append(processes[i])
							start=now
							
					else:
						if(processes[i].priority<running[0].priority):
							temp_turn=turn(start,now)
							running[0].turns.append(temp_turn)
							running[0].burst_time=running[0].burst_time-(now-start)
							ready.append(running[0])
							sort_by("priority",ready)
							running.pop()
							running.append(processes[i])
							start=now
						else:
							ready.append(processes[i])
							sort_by("priority",ready)
				i=i+1
			    
				
			if(len(running)>0 and running[0].burst_time!=0):
				now=start+running[0].burst_time
				temp_turn=turn(start,now)
				running[0].turns.append(temp_turn)	
				running[0].burst_time=0
				running[0].done=1
				running.pop()

			while(len(ready)>0):
				running.append(ready[0])
				ready.pop(0)
				start=now
				now=start+running[0].burst_time
				temp_turn=turn(start,now)
				running[0].turns.append(temp_turn)	
				running[0].burst_time=0
				running[0].done=1
				running.pop()

			if(len(running)>0 and running[0].burst_time!=0):
				now=start+running[0].burst_time
				temp_turn=turn(start,now)
				running[0].turns.append(temp_turn)	
				running[0].burst_time=0
				running[0].done=1
				running.pop()	







							




		elif(schuduling_type=="Priority (Non Preemptive)"):
			now=0
			finished=0;
			while  finished<len(processes):
				sort_by("priority",processes)
				flag=0
				for p in processes:
					start=now
					if(p.arrival_time<=now and p.done==0):
						if(now<p.arrival_time):
							start=p.arrival_time
						temp_turn=turn(start,start+p.burst_time)
						p.turns.append(temp_turn)
						now=now+p.burst_time
						p.done=1
						finished=finished+1
						flag=1
						break
				if(flag==0):
					sort_by("arrival_time",processes)
					for p in processes:
						if(p.done==0):
							now=p.arrival_time;
							break

		elif(schuduling_type=="Round Robin"):
			now=0
			finished=0
			sort_by("arrival_time",processes)
			while finished<len(processes):
				flag=0
				for p in processes:
					start=now
					RR_duration=quant_time

					if(p.arrival_time<=now and p.done==0):
						#print(p.name," ",start ," ",RR_duration)
						if(now<p.arrival_time):
							start=p.arrival_time
						if(RR_duration>p.burst_time):
							RR_duration=p.burst_time
						temp_turn=turn(start,start+RR_duration)
						p.turns.append(temp_turn)
						p.burst_time=p.burst_time-RR_duration
						if(p.burst_time<=0):
							p.done=1
							finished=finished+1
						now=now+RR_duration
						flag=1
						
				if(flag==0):
					for p in processes:
						if(p.done==0):
							now=p.arrival_time;
							break
					
		
		T=Toplevel()
		T.title('Time Line')
		T.config(bg='lavender')
		my_height=150
		my_width=600
		My_Canvas=Canvas(T,height=my_height,width=my_width+25,bd=0,highlightbackground="black",highlightthickness=0,bg="lightblue")
		My_Canvas.pack(fill=X,side=TOP)
		My_Canvas.create_text(0,my_height,text='0',font="times 9 bold",anchor='sw')
		sum=0
		for e in processes:
			if(e.turns[-1].finish>sum):
				sum=e.turns[-1].finish
		if(sum==0):
			sum=1
		colors=['red','yellow','DodgerBlue','orange','hot pink','salmon2','turquoise2']
		i=0	
		for e in range(len(processes)):		
			for f in range(len(processes[e].turns)):
				if(processes[e].turns[f].start==processes[e].turns[f].finish):
					continue
				My_Canvas.create_rectangle((float(processes[e].turns[f].start)/sum)*my_width,0,(float(processes[e].turns[f].finish)/sum)*my_width,my_height,fill=colors[i])
				My_Canvas.create_text((float(processes[e].turns[f].start)/sum)*my_width,my_height,text='{:g}'.format(processes[e].turns[f].start),font="times 9 bold",anchor="sw")
				My_Canvas.create_text((float(processes[e].turns[f].finish+processes[e].turns[f].start)/(2*sum))*my_width,my_height/2,text=processes[e].name+' ',font="times 12 bold")
				My_Canvas.create_text((float(processes[e].turns[f].finish)/sum)*my_width,my_height,text='{:g}'.format(processes[e].turns[f].finish),font="times 9 bold",anchor="sw")
				i=i+1
				if(i==len(colors)):
					i=0

		result=[]
		calc_Turnaround_waiting_time(processes,backup,result)
		Label(T,text=schuduling_type+" Scheduling Type",font="times 12 bold",bg='lavender',fg='red').pack()
		Label(T,text="Average Waiting Time =  "+'{:g}'.format((result[0])),font="times 12 bold",bg='lavender',fg='red').pack()
		Label(T,text="Average Turnaround Time =  "+'{:g}'.format((result[1])),font="times 12 bold",bg='lavender',fg='red').pack()
	except TclError:
				print ('\007')		
 

	

			
		
def my_robin(event):
	global QU,quantum
	quantum.grid_forget()
	QU.grid_forget()

	if(combobox.get()=='Round Robin'):
		QU.grid(row=12,column=0,columnspan=1,sticky='e')
		quantum.grid(row=12,column=0,sticky='w')
	
	for e in range(len(Entry_list)):
		if(combobox.get()=='Priority (Preemptive)' or combobox.get()=='Priority (Non Preemptive)'):
			Entry_list[e][2].config(state='normal',bg='white')
		else:
			Entry_list[e][2].config(state='disabled',disabledbackground='gray84')		
def Table():
	try:
		del Entry_list[:]
		list = table.grid_slaves()
		for e in list:
			e.destroy()
		
		e=0
		for e in range(No_of_processes.get()):
			Label(table,text="P"+str(e+1)+'',font="Helvetica 10 bold",bg='lightyellow1').grid(row=e+3,column=0,columnspan=1)
		Entries()
		if(No_of_processes.get()>0):
			Label(table,text="Arrival time",font="Helvetica 10 bold",bg='lightyellow1').grid(row=1,column=1)	
			Label(table,text="CPU Burst",font="Helvetica 10 bold",bg='lightyellow1').grid(row=1,column=2)
			Label(table,text="Priority",font="Helvetica 10 bold",bg='lightyellow1').grid(row=1,column=3)
			Button(table,text="Clear",command=clear,font="Times 11 bold",bg='salmon',fg='lightblue').grid(column=3,row=e+4,rowspan=2)	
			Button(table,text="Schedule",command=schedule,font="Times 11 bold",bg='salmon',fg='lightblue').grid(column=0,row=e+4,rowspan=2)
	except TclError:
		print ('\007')		
def Entries():
	global Entry_list
	global Entry_variables
	for e in range(No_of_processes.get()):
		variable1=DoubleVar()
		variable1.set(0)
		variable2=DoubleVar()
		variable2.set(0)
		variable3=DoubleVar()
		variable3.set(0)
		Entry_variables.append((variable1,variable2,variable3))
		Entry_list.append((Entry(table,width=6,textvariable=Entry_variables[e][0]),Entry(table,width=6,textvariable=Entry_variables[e][1]),Entry(table,width=6,textvariable=Entry_variables[e][2])))
		Entry_list[e][0].grid(row=e+3,column=1)
		Entry_list[e][1].grid(row=e+3,column=2)
		Entry_list[e][2].grid(row=e+3,column=3)
		if(combobox.get()!='Priority (Preemptive)' and combobox.get()!='Priority (Non Preemptive)'):
			Entry_list[e][2].config(state='disabled',disabledbackground='gray84')

def clear():
	for e in range(len(Entry_list)):
		for k in range(len(Entry_list[e])):	
			Entry_variables[e][k].set(0)

#I-------------------------------------------------------------------I
#I-------------------------------------------------------------------I			
WINDOW=Tk()
WINDOW.title("Scheduler")
WINDOW.config()
Label(WINDOW,bg='lavender').grid(column=0)
Label(WINDOW,bg='lavender').grid(column=1)
Label(WINDOW,bg='lavender').grid(column=3,row=0)
Label(WINDOW,bg='lavender').grid(column=4,row=0)
root=Frame(WINDOW)
root.grid(column=2,row=1)
root.config(bg='lavender')
No_of_processes=IntVar()
Number_of_processes=Entry(root,textvariable=No_of_processes)
Number_of_processes.grid(row=0,column=1,columnspan=1,sticky='w')
Label(root,text="Number of processes: ",bg='lavender',fg='red',font='Helvetica 9 bold').grid(row=0,column=0,columnspan=1,sticky='w')
Label(root,text="Scheduling Algortihm: ",bg='lavender',fg='red',font='Helvetica 9 bold').grid(row=1,column=0,columnspan=1,sticky='w')
choices = ['FCFS', 'SJF (Preemptive)', 'SJF (Non Preemptive)','Priority (Preemptive)','Priority (Non Preemptive)','Round Robin']
variable = StringVar()
variable.set('FCFS')
combobox = ttk.Combobox(root,values = choices,textvariable=variable)
combobox.grid(row=1,column=1,sticky='w')
combobox.bind("<<ComboboxSelected>>",my_robin)
Button(root,text="Create Table",command=Table,bg='salmon',fg='light blue',font="Times 11 bold").grid(column=0,columnspan=1,sticky='w')
table=Frame(root,height=200,width=300,bd=2,highlightcolor="red",highlightthickness=1,relief=SOLID,bg='lightyellow1')
table.grid(column=0,columnspan=1,sticky='w')
Entry_list=[]
Entry_variables=[]
Entry_list.append((Entry(table),Entry(table),Entry(table)))
quantum_var=DoubleVar()
quantum_var.set(1)
QU=Entry(root,width=5,textvariable=quantum_var)
quantum=Label(root,text="Time Quantum: ",font="Helvetica 10 bold")
WINDOW.mainloop()
