import { ListaLogComponent } from './lista-log/lista-log.component';
import { CommonModule } from '@angular/common';
import { FormLogComponent } from './form-log/form-log.component';
import { AppRoutingModule } from './app-routing.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NotifierModule, NotifierOptions, NotifierService } from 'angular-notifier';
import {NgxMaskModule} from 'ngx-mask';
import { OrderModule } from 'ngx-order-pipe';
import { NgxPaginationModule } from 'ngx-pagination';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ErrorsModule } from './errors/errors.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Ng2SearchPipeModule } from 'ng2-search-filter';
import { FilterPipeModule } from 'ngx-filter-pipe';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';


const customNotifierOptions: NotifierOptions = {
  position: {
    horizontal: {
      position: 'right',
      distance: 12
    },
    vertical: {
      position: 'top',
      distance: 75,
      gap: 10
    }
  },
  theme: 'material',
  behaviour: {
    autoHide: 5000,
    onClick: 'hide',
    onMouseover: 'pauseAutoHide',
    showDismissButton: true,
    stacking: 4
  },
  animations: {
    enabled: true,
    show: {
      preset: 'slide',
      speed: 300,
      easing: 'ease'
    },
    hide: {
      preset: 'fade',
      speed: 300,
      easing: 'ease',
      offset: 50
    },
    shift: {
      speed: 300,
      easing: 'ease'
    },
    overlap: 150
  }
};

@NgModule({
  declarations: [
    AppComponent,
    FormLogComponent,
    ListaLogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ErrorsModule,
    NotifierModule.withConfig(customNotifierOptions),
    NgxMaskModule.forRoot(),
    OrderModule,
    FormsModule,
    ReactiveFormsModule,
    NgxPaginationModule,
    FilterPipeModule,
  
    CommonModule,
    Ng2SearchPipeModule,
    NoopAnimationsModule,


  ],
 
  providers: [NotifierService],
  bootstrap: [AppComponent]
})
export class AppModule { }
