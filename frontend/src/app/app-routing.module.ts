import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FilesComponent } from './files/files.component';
import { HouseComponent } from './house/house.component';
import { LoginComponent } from './login/login.component';
import { ResultComponent } from './result/result.component';

const routes: Routes = [
  {path:'',component:LoginComponent},
  {path:'files',component:FilesComponent},
  {path:'house',component:HouseComponent},
  {path:'refresh',component:LoginComponent},
  {path:'result',component:ResultComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
