import { Component, OnInit } from '@angular/core';
import { ServerService } from '../server.service';


@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  constructor(private _priceService:ServerService) { }
  price:any;
  ngOnInit(): void {
    this.price=this._priceService.getPrice();
    console.warn(this.price)
  }
 

}
