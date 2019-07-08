import { FormsModule } from '@angular/forms';
import { NgxSpinnerModule } from 'ngx-spinner';
import { FormLogComponent } from './form-log/form-log.component';
import { ListaLogComponent } from './lista-log/lista-log.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';


const routes: Routes = [
    
  { path: 'lista-log', component: ListaLogComponent },
  { path: 'form-log', component: FormLogComponent },
];

@NgModule({
  imports: [ 
      RouterModule.forRoot(routes),
      NgxSpinnerModule,
      FormsModule,
      HttpClientModule
  ],
  exports: [ RouterModule,NgxSpinnerModule ]
})
export class AppRoutingModule { }
