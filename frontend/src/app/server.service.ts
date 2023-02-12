import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class ServerService {
  private _url:string ='http://127.0.0.1:5000/files';
  private _url2:string ='http://127.0.0.1:5000/verifyUser';
  private _url3:string ='http://127.0.0.1:5000/house';
  
  
  constructor(private http:HttpClient) { }
  housePrice:any;
  fileUpload(file:any){
    const fd=new FormData();
    fd.append('csv',file,file.name)
    
    return this.http.post<any>(this._url,fd)
  }
  
  verifyUser(data:any){
    return  this.http.post<any>(this._url2, data);
  }
  
  houseProcess(data:any){
    return this.http.post<any>(this._url3,data);
  }
  
  setPrice(data:any){
    console.warn(data.Result)
    this.housePrice=data.Result;
  }

  getPrice(){
     return this.housePrice;
  }

}
