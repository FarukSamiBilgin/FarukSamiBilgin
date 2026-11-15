// Overdamped RSJ under microwave drive; normalised short-junction CPR (tau). Writes shapiro.json.
function cpr(tau){const N=4096,t=new Float64Array(N);let m=0;for(let k=0;k<N;k++){const p=2*Math.PI*k/N,v=Math.sin(p)/Math.sqrt(1-tau*Math.sin(p/2)**2);t[k]=v;if(v>m)m=v;}for(let k=0;k<N;k++)t[k]/=m;return p=>{let x=p/(2*Math.PI);x-=Math.floor(x);return t[(x*N)|0];};}
function iv(f,iac,W,ib){const T=2*Math.PI/W,spp=200,dt=T/spp;let phi=0,t=0;const run=n=>{for(let k=0;k<n*spp;k++){const a=ib-f(phi)+iac*Math.sin(W*t),b=ib-f(phi+dt*a)+iac*Math.sin(W*(t+dt));phi+=dt*(a+b)/2;t+=dt;}};run(10);const p0=phi;run(40);return (phi-p0)/(40*T)/W;}
const f=cpr(0.95),out=[];for(let i=0;i<=200;i++){const ib=i*5/200;out.push([ib,iv(f,2,2,ib)]);}
require('fs').writeFileSync(__dirname+'/shapiro.json',JSON.stringify(out));console.log('ok',out.length);
