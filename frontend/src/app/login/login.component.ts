import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { ServerService } from '../server.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private _LoginService:ServerService,private router:Router ) { }
  submitted:any;
  ngOnInit(): void {
  }
  onSubmit(data:any){
    console.warn(data)
   this._LoginService.verifyUser(data).subscribe(
       da => this.onResponse(da), 
       error => console.log('Error!',error)
     )
   
    
  }
  onResponse(data:any){
      if(data.result == true ){
        this.router.navigateByUrl('/files');
      }else{
        console.profile('error popup')
        this.router.navigateByUrl('/refresh');
      }
  }
}
