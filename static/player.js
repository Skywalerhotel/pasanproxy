let video=document.getElementById("video")

document.getElementById("play").onclick=()=>{
if(video.paused) video.play()
else video.pause()
}

function seek(s){
video.currentTime+=s
}

function toggleFullscreen(){
if(!document.fullscreenElement)
video.requestFullscreen()
else
document.exitFullscreen()
}

function toggleSettings(){
let s=document.getElementById("settings")
s.style.display=s.style.display=="block"?"none":"block"
}

document.getElementById("speed").onchange=function(){
video.playbackRate=this.value
}

document.getElementById("srt").addEventListener("change",function(){
let file=this.files[0]
let url=URL.createObjectURL(file)
let track=document.createElement("track")
track.kind="subtitles"
track.src=url
track.default=true
video.appendChild(track)
})

fetch("/tracks?url="+encodeURIComponent(VIDEO_URL))
.then(r=>r.json())
.then(data=>{
let audio=document.getElementById("audio")
let subs=document.getElementById("subs")
data.audio.forEach(a=>{
let o=document.createElement("option")
o.text="Audio "+a.lang
audio.add(o)
})
data.subs.forEach(s=>{
let o=document.createElement("option")
o.text="Subtitle "+s.lang
subs.add(o)
})
})