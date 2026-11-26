// Doré Offline: dependency-free, loopback-only presentation runtime.
package main
import (
 "flag"
 "fmt"
 "log"
 "mime"
 "net"
 "net/http"
 "os"
 "os/exec"
 "path/filepath"
 "regexp"
 "strings"
 "time"
)
const addr = "127.0.0.1:8765"
const csp = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; media-src 'self' blob: data:; worker-src 'self' blob:; frame-src 'self' blob:; object-src 'none'; base-uri 'self'"
func snapshot(home string) (string,error) {
 b,e:=os.ReadFile(filepath.Join(home,"current")); if e!=nil{return "",e}
 sha:=strings.TrimSpace(string(b))
 if !regexp.MustCompile("^[0-9a-f]{40}$").MatchString(sha){return "",fmt.Errorf("invalid snapshot version")}
 root,e:=filepath.EvalSymlinks(filepath.Join(home,"versions",sha,"site")); if e!=nil{return "",e}
 root,e=filepath.Abs(root); if e!=nil{return "",e}
 for _,name:=range []string{"index.html","one/index.html","olive/index.html"}{
  st,e:=os.Stat(filepath.Join(root,name)); if e!=nil||!st.Mode().IsRegular()||st.Size()==0{return "",fmt.Errorf("missing route: %s",name)}
 }
 return root,nil
}
func handler(root string) http.Handler {
 return http.HandlerFunc(func(w http.ResponseWriter,r *http.Request){
  w.Header().Set("Content-Security-Policy",csp)
  w.Header().Set("X-Content-Type-Options","nosniff")
  if r.Host!=addr && r.Host!="localhost:8765" {http.Error(w,"Local access only",403);return}
  if r.Method!=http.MethodGet&&r.Method!=http.MethodHead{http.Error(w,"Read only",405);return}
  if strings.ContainsAny(r.URL.Path,"\\\x00"){http.NotFound(w,r);return}
  for _,part:=range strings.Split(r.URL.Path,"/"){if part==".."||part=="."{http.NotFound(w,r);return}}
  path:=filepath.Join(root,filepath.FromSlash(strings.TrimPrefix(r.URL.Path,"/")))
  real,e:=filepath.EvalSymlinks(path)
  if e!=nil{http.NotFound(w,r);return}
  rel,e:=filepath.Rel(root,real)
  if e!=nil||rel==".."||strings.HasPrefix(rel,".."+string(os.PathSeparator)){http.NotFound(w,r);return}
  if st,e:=os.Stat(real);e==nil&&st.IsDir(){
   if !strings.HasSuffix(r.URL.Path,"/"){http.Redirect(w,r,r.URL.Path+"/",http.StatusMovedPermanently);return}
   real,e=filepath.EvalSymlinks(filepath.Join(real,"index.html"));if e!=nil{http.NotFound(w,r);return}
   rel,e=filepath.Rel(root,real);if e!=nil||rel==".."||strings.HasPrefix(rel,".."+string(os.PathSeparator)){http.NotFound(w,r);return}
  }
  f,e:=os.Open(real);if e!=nil{http.NotFound(w,r);return};defer f.Close()
  st,e:=f.Stat();if e!=nil||!st.Mode().IsRegular(){http.NotFound(w,r);return}
  switch strings.ToLower(filepath.Ext(real)){
  case ".wasm":w.Header().Set("Content-Type","application/wasm")
  case ".glb":w.Header().Set("Content-Type","model/gltf-binary")
  case ".gltf":w.Header().Set("Content-Type","model/gltf+json")
  case ".js",".mjs":w.Header().Set("Content-Type","text/javascript")
  default:if typ:=mime.TypeByExtension(filepath.Ext(real));typ!=""{w.Header().Set("Content-Type",typ)}
  }
  http.ServeContent(w,r,st.Name(),st.ModTime(),f)
 })
}
func main(){
 home:=flag.String("home","","portable-data directory")
 noOpen:=flag.Bool("no-open",false,"do not open browser")
 flag.Parse()
 if *home==""{log.Fatal("Missing -home")}
 root,e:=snapshot(*home);if e!=nil{log.Fatal(e)}
 ln,e:=net.Listen("tcp",addr);if e!=nil{log.Fatal("Cannot start local presentation (port 8765): ",e)}
 defer ln.Close()
 server:=&http.Server{Handler:handler(root),ReadHeaderTimeout:5*time.Second,IdleTimeout:60*time.Second,MaxHeaderBytes:1<<16}
 fmt.Println("Doré Offline · http://"+addr+" · Ctrl-C to stop")
 if !*noOpen{if e:=exec.Command("/usr/bin/open","http://"+addr).Start();e!=nil{log.Print("Open browser manually: http://"+addr)}}
 if e:=server.Serve(ln);e!=nil&&e!=http.ErrServerClosed{log.Fatal(e)}
}
