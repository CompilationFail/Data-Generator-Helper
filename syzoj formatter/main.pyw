import os,shutil,time
from tkinter import * 

Bgcolor="lightskyblue"
Labelcolor="azure"
Buttoncolor="lightgray"
Font=("consolas",10,"normal")

top=Tk()
top.title("  HydroOJ Data Formatter")
top.configure(bg=Bgcolor)

TL=Entry(top)
ML=Entry(top)
FILE=Entry(top)

_time=""
_memory=""
_file=""

def yaml_prefix():
	global _file,_time,_memory
	print(_time,_memory,_file,"!")
	res="type: default\n"
	res+=("time: %s\n"%_time)
	res+=("memory: %s\n"%_memory)
	res+="checker_type: default\n"

	if _file!="":
		res+="filename: %s\n"%(_file)
	res+="\nlangs:\n"
	res+="  - cc.cc11o2\n  - cc.cc14o2\n  - cc.cc17o2"
	res+="\n\n"
	return res

def clear_all():
	global TL,ML,FILE,_time,_memory,_file,top
	_time=TL.get()
	_memory=ML.get()
	_file=FILE.get()
	global top
	for child in top.winfo_children():
		child.destroy()


def split_suffix(s):
	if s.find(".")==-1: return (s,"")
	p=0
	while True:
		q=s.find(".",p+1)
		if q==-1: break
		p=q
	return (s[:p],s[p+1:])

def search(path):
	#print("search",path)
	res=[]
	#print("search",path)
	def dfs(path):
		#print(path)
		if os.path.isfile(path):
			res.append(path)
			return
		for i in os.listdir(path):
			dfs(os.path.join(path,i))
	dfs(path)
	return res

def match_files(path):
	inp_dic=["in"]
	outp_dic=["out","ans"]
	dic={}
	for i in search(path):
		a,b=split_suffix(i)
		if not a in dic.keys():
			dic[a]=["",""]
		if b in inp_dic:
			dic[a][0]=i
		if b in outp_dic:
			dic[a][1]=i
	res=[]
	for i in dic.keys():
		t=dic[i]
		if t[0]!="" and t[1]!="":
			res.append(t)
	return res

def load_subtask():
	global _time,_memory,Bgcolor,Labelcolor,Buttoncolor,top,Font
	clear_all()
	fmt="  - score: %d\n    type: %s\n    time: %s\n    memory: %s\n    cases:\n%s"
	cas_fmt="      - input: %s\n        output: %s\n"

	def Move_And_Rename(path,id,score,typ):
		print("Move and Rename ",path,id,score,typ)
		dic={}
		cases=""
		files=match_files(path)

		for a,b in files:
			c,d=os.path.split(a)[1],os.path.split(b)[1]
			c="%d-%s" % (id,c)
			d="%d-%s" % (id,d)
			shutil.move(a,c)
			shutil.move(b,d)
			cases+=cas_fmt%(c,d)	

		if cases=="":
			return ""
		return fmt % (score,typ,_time,_memory,cases)

	curheight=10
	H=30
	D=200 # width of folder name label
	M=15  
	L=20
	D2=80 # width  of input box
	lis=[]
	D3=50 # choose button width


	Label(top,text="folder name",bg=Labelcolor,font=Font).place(y=curheight,x=L,height=H,width=D)
	Label(top,text="score",bg=Labelcolor,font=Font).place(y=curheight,x=L+D+M,height=H,width=D2)
	Label(top,text="type",bg=Labelcolor,font=Font).place(y=curheight,x=L+D+M+D2+M,height=H,width=D3*3)

	curheight+=H+M
	defaultscore="0"
	defaulttype=0 # min,sum,mul 

	for i in os.listdir():
		if os.path.isfile(i): continue
		lbl=Label(top,text=i,bg=Labelcolor,font=Font)
		lbl.place(y=curheight,x=L,height=H,width=D)
		inp1=Entry(top)
		inp1.insert(0,defaultscore)
		inp1.place(y=curheight,x=L+D+M,height=H,width=D2)
		inp2=Frame(top,bg=Labelcolor)
		inp2.place(y=curheight,x=L+D+M+D2+M,height=H,width=D3*3)
		ch=IntVar()
		ch.set(0)
		Radiobutton(inp2, variable=ch, text="min", value=0,bg=Labelcolor,font=Font).place(y=0,x=0)
		Radiobutton(inp2, variable=ch, text="sum", value=1,bg=Labelcolor,font=Font).place(y=0,x=D3)
		Radiobutton(inp2, variable=ch, text="max", value=2,bg=Labelcolor,font=Font).place(y=0,x=D3*2)
		curheight+=H+M
		lis.append([i,inp1,ch])
		#GetFormat(i)
	curheight+=M*2

	def Run():
		res=yaml_prefix()+"subtasks:\n"
		cnt=0
		for i in lis:
			cnt+=1
			try:
				score=int(i[1].get())
			except:
				score=defaultscore
			if score>100: score=100
			if score<0: score=0
			res+=Move_And_Rename(i[0],cnt,score,["min","sum","max"][i[2].get()])
			try:
				os.rmdir(i[0])
			except:
				pass

		with open("config.yaml","w") as outp:
			outp.write(res)
		time.sleep(1)
		top.quit()
		exit(0)

	btn=Button(text="Format!",command=Run,bg=Buttoncolor,font=Font)
	btn.place(y=curheight,x=(L+D+M+D2+M+D3*3+L-D-D2)/2,height=H*2,width=D+D2)
	curheight+=H*2+M*3


	top.geometry('%dx%d' % (L+D+M+D2+M+D3*3+L,curheight))


def load_none_subtask():
	global _time,_memory,Bgcolor,Labelcolor,Buttoncolor,top
	clear_all()
	fmt="  - score: %d\n    type: %s\n    time: %s\n    memory: %s\n    cases:\n%s"
	cas_fmt="      - input: %s\n        output: %s\n"
	cases=""
	for (a,b) in match_files(os.path.split(os.path.realpath(__file__))[0]):
		#print(a,b)
		c,d=os.path.split(a)[1],os.path.split(b)[1]
		cases+=cas_fmt%(c,d)	

	res=yaml_prefix()+"subtasks:\n"+fmt%(100,"sum",_time,_memory,cases)
	#print(res)
	with open("config.yaml","w") as outp:
		outp.write(res)

	time.sleep(1)
	top.quit()
	exit(0)




def load_initial():
	global _time,_memory,Bgcolor,Labelcolor,Buttoncolor,top
	curheight=10
	H=30
	D=250 # width of folder name label
	M=15  
	L=20
	D2=80 # width  of input box
	lis=[]
	D3=50 # choose button width
	D4=160

	Label(top,text="时间限制",bg=Labelcolor,font=Font).place(y=curheight,x=L,height=H,width=D4)
	Label(top,text="空间限制",bg=Labelcolor,font=Font).place(y=curheight,x=L+D4+M,height=H,width=D4)
	Label(top,text="文件评测(选填)",bg=Labelcolor,font=Font).place(y=curheight,x=L+D4*2+M*2,height=H,width=D4)
	curheight+=H+M


	TL.place(y=curheight,x=L,height=H,width=D4)
	TL.insert(0,"1000ms")
	ML.place(y=curheight,x=L+D4+M,height=H,width=D4)
	ML.insert(0,"256m")
	FILE.place(y=curheight,x=L+D4*2+M*2,height=H,width=D4)
	curheight+=H+M*2

	btn=Button(text="no subtask",command=load_none_subtask,bg=Buttoncolor,font=Font)
	btn.place(y=curheight,x=L,height=H*2,width=D)
	btn=Button(text="subtask",command=load_subtask,bg=Buttoncolor,font=Font)
	btn.place(y=curheight,x=L+D+M,height=H*2,width=D)

	curheight+=H+M*3

	top.geometry('%dx%d' % (L+D+M+D2+M+D3*3+L,curheight))

load_initial()
mainloop()

