import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServerService } from '../server.service';

@Component({
  selector: 'app-files',
  templateUrl: './files.component.html',
  styleUrls: ['./files.component.css']
})
export class FilesComponent implements OnInit {

  constructor(private _FileService:ServerService,private router:Router) { }
  public selectedFile = null;
  ngOnInit(): void {
  }
  onFileSelected(event:any){
      console.log(event)
      this.selectedFile = event.target.files[0];
  }
  onUpload(){
    console.log(this.selectedFile)
    this._FileService.fileUpload(this.selectedFile).subscribe(
      da => this.dataEntry(da),
      error => console.log('Error!',error)
    )
      
  }
  dataEntry(data:any){
    if(data.result == true){
      this.router.navigateByUrl('/house');
    }else{
     
    }
  }
}
