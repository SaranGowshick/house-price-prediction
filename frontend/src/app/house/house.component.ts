import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-house',
  templateUrl: './house.component.html',
  styleUrls: ['./house.component.css']
})
export class HouseComponent implements OnInit {
  result:any;
  constructor(private _HouseService:ServerService,private router:Router) { }

  ngOnInit(): void {
  }
  onSubmit(data:any){
    console.warn(data)
    this._HouseService.houseProcess(data).subscribe(
      da => this.onResponse(da),
      error => console.log('Error!',error)
    )
  }
  onResponse(data:any){
        console.warn(data)
        this._HouseService.setPrice(data);
        if(data.Result== false){
            this.router.navigateByUrl('/files');
        }else{
        this.router.navigateByUrl('/result');
  
      }

    }
  }