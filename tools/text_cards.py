from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def card(name, lines, y=330, credit=None):
    im=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    for text,size,col in lines:
        f=ImageFont.truetype(F,size)
        w=d.textbbox((0,0),text,font=f,stroke_width=8)[2]
        d.text(((1080-w)//2,y),text,font=f,fill=col,stroke_width=8,stroke_fill="#120830")
        y+=int(size*1.25)
    if credit:
        f=ImageFont.truetype(F,30); w=d.textbbox((0,0),credit,font=f)[2]
        d.text(((1080-w)//2,1760),credit,font=f,fill=(255,255,255,200),stroke_width=3,stroke_fill="#120830")
    im.save(name)
P,C,G,W="#ff3caa","#3cf0ff","#ffd65a","#ffffff"
card("t1.png",[("PEOPLE ON",110,W),("19 NOVEMBER:",110,P)])
card("t2.png",[("PEOPLE ON",110,W),("19 NOVEMBER:",110,P),("stuck in traffic 🚗".replace(" 🚗",""),70,C)])
card("t3.png",[("PEOPLE ON",110,W),("19 NOVEMBER:",110,P),("at work all day",70,C)])
card("t4.png",[("ME ON",130,W),("19 NOVEMBER:",130,G)],y=760)
card("t5.png",[("ME ON 19 NOV:",90,G)],credit="Footage: Rockstar Games official trailer + Pixabay")
card("t6.png",[("Comment VICE if",80,W),("you're calling in sick",80,P)],y=300,credit="Footage: Rockstar Games official trailer + Pixabay")
