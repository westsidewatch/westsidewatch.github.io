package main
import("net/http/httptest";"os";"path/filepath";"testing")
func TestReadOnlyRangesAndIsolation(t *testing.T){
 root:=t.TempDir()
 if e:=os.WriteFile(filepath.Join(root,"index.html"),[]byte("0123456789"),0600);e!=nil{t.Fatal(e)}
 outside:=filepath.Join(t.TempDir(),"secret");if e:=os.WriteFile(outside,[]byte("secret"),0600);e!=nil{t.Fatal(e)}
 if e:=os.Symlink(outside,filepath.Join(root,"escape"));e!=nil{t.Fatal(e)}
 h:=handler(root)
 for _,x:=range []struct{method,path,host,rg string;code int;body string}{
 {"GET","/",addr,"bytes=2-5",206,"2345"},
 {"GET","/escape",addr,"",404,""},
 {"GET","/missing",addr,"",404,""},
 {"POST","/",addr,"",405,""},
 {"GET","/","example.com","",403,""},
 }{
  req:=httptest.NewRequest(x.method,"http://"+x.host+x.path,nil);req.Header.Set("Range",x.rg)
  rec:=httptest.NewRecorder();h.ServeHTTP(rec,req)
  if rec.Code!=x.code{t.Fatalf("%s: got %d expected %d",x.path,rec.Code,x.code)}
  if x.body!=""&&rec.Body.String()!=x.body{t.Fatal(rec.Body.String())}
  if rec.Header().Get("Content-Security-Policy")==""{t.Fatal("missing CSP")}
 }
}
