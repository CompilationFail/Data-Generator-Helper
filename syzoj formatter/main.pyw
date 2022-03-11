import os,shutil,time
from tkinter import * 

Bgcolor="lightskyblue"
Labelcolor="azure"
Buttoncolor="lightgray"

top=Tk()
top.title("  SYZOJ Data Formatter")
top.configure(bg=Bgcolor)

fmt="  - score: %d\n    type: %s\n    cases: %s"

def Search(path):
	#print("search",path)
	res=[]
	def dfs(path):
		#print(path)
		if os.path.isfile(path):
			res.append(path)
			return
		for i in os.listdir(path):
			dfs(os.path.join(path,i))
	dfs(path)
	return res

def GetName(s):
	if s.find(".")==-1: return (s,"")
	p=0
	while True:
		q=s.find(".",p+1)
		if q==-1: break
		p=q
	return ("'"+s[:p]+"'",s[p+1:])

inpdict=["in",""]
oupdict=["out","ans","a"]
inpformat="in"
oupformat="ans"

def Move_And_Rename(path,id,score,typ):
	print("Move and Rename ",path,id,score,typ)
	dic={}
	for i in Search(path):
		print("Moved ",i)
		a,b=os.path.split(i)
		name=str(id)+"-"+b
		npath=name
		x,y=GetName(name)
		dic[x]=""
		#lis.append("'"+name+"'")
		#print(i,npath)
		shutil.move(i,npath)
	return fmt % (score,typ,'['+','.join(dic.keys())+']')+"\n"

curheight=10
H=30
D=250 # width of folder name label
M=15  
L=20
D2=80 # width  of input box
lis=[]
D3=50 # choose button width


Label(top,text="folder name",bg=Labelcolor,font=("consolas",10,"normal")).place(y=curheight,x=L,height=H,width=D)
Label(top,text="score",bg=Labelcolor,font=("consolas",10,"normal")).place(y=curheight,x=L+D+M,height=H,width=D2)
Label(top,text="type",bg=Labelcolor,font=("consolas",10,"normal")).place(y=curheight,x=L+D+M+D2+M,height=H,width=D3*3)

curheight+=H+M
initial_height=curheight
defaultscore="0"
defaulttype=0 # min,sum,mul 
maxcurheight=0
curx=0
cnt=0
for i in os.listdir():
	if os.path.isfile(i): continue
	if cnt==10:
		maxcurheight=curheight
		cnt=0
		curx+=L+D+M+D2+M+D3*3+L+M
		curheight=initial_height
	cnt+=1
	lbl=Label(top,text=i,bg=Labelcolor,font=("consolas",10,"normal"))
	lbl.place(y=curheight,x=curx+L,height=H,width=D)
	inp1=Entry(top)
	inp1.insert(0,defaultscore)
	inp1.place(y=curheight,x=curx+L+D+M,height=H,width=D2)
	inp2=Frame(top,bg=Labelcolor)
	inp2.place(y=curheight,x=curx+L+D+M+D2+M,height=H,width=D3*3)
	ch=IntVar()
	ch.set(0)
	Radiobutton(inp2, variable=ch, text="min", value=0,bg=Labelcolor,font=("consolas",10,"normal")).place(y=0,x=0)
	Radiobutton(inp2, variable=ch, text="sum", value=1,bg=Labelcolor,font=("consolas",10,"normal")).place(y=0,x=D3)
	Radiobutton(inp2, variable=ch, text="mul", value=2,bg=Labelcolor,font=("consolas",10,"normal")).place(y=0,x=D3*2)
	curheight+=H+M
	lis.append([i,inp1,ch])
	#GetFormat(i)

curx+=L+D+M+D2+M+D3*3+L

maxcurheight=max(maxcurheight,curheight)
print(maxcurheight)
maxcurheight+=M*2

Label(top,text="input file",bg=Labelcolor,font=("consolas",10,"normal")).place(y=maxcurheight,x=(curx-D*2-M)/2,height=H,width=D)
Label(top,text="output file",bg=Labelcolor,font=("consolas",10,"normal")).place(y=maxcurheight,x=(curx-D*2-M)/2+D+M,height=H,width=D)
maxcurheight+=H+M
IN=Entry(top)
IN.place(y=maxcurheight,x=(curx-D*2-M)/2,height=H,width=D)
IN.insert(0,"#."+inpformat)
OUT=Entry(top)
OUT.place(y=maxcurheight,x=(curx-D*2-M)/2+D+M,height=H,width=D)
OUT.insert(0,"#."+oupformat)
maxcurheight+=H+M
spjbutton=IntVar()
spjbutton.set(0)
Checkbutton(top, variable=spjbutton,onvalue = 1, offvalue = 0, text="special judge   default:spj language: cpp17, \n option                 spj file:    spj.cpp ", 
	bg=Labelcolor,font=("consolas",10,"normal"),height=4,width=50).place(y=maxcurheight,x=(curx-380)/2)
#Label(top,text="",bg=Labelcolor,font=("consolas",10,"normal")).place(y=curheight,x=L+D2+D3+M,height=H*2,width=D)

maxcurheight+=H+M*4
IDSTART=1


def Run():
	global IN,OUT,IDSTART,inpformat,oupformat,spjbutton
	res="subtasks:\n"
	cnt=IDSTART
	for i in lis:
		try:
			score=int(i[1].get())
		except:
			score=defaultscore
		if score>100: score=100
		if score<0: score=0
		res+=Move_And_Rename(i[0],cnt,score,["min","sum","mul"][i[2].get()])
		cnt+=1
		try:
			os.rmdir(i[0])
		except:
			pass
	res+="\n\n"
	res+="inputFile: '%s'\noutputFile: '%s'" % (IN.get(),OUT.get())
	res+="\n\n"
	if spjbutton.get()==1:
		res+="specialJudge:\n  language: cpp17\n  fileName: spj.cpp"
	with open("data.yml","w") as outp:
		outp.write(res)
	time.sleep(1)
	top.quit()
	exit(0)





btn=Button(text="Format!",command=Run,bg=Buttoncolor,font=("consolas",10,"normal"))
btn.place(y=maxcurheight,x=(curx-D-D2)/2,height=H*2,width=D+D2)
maxcurheight+=H*2+M*2


top.geometry('%dx%d' % (curx,maxcurheight))

print(curx,maxcurheight)

mainloop()





