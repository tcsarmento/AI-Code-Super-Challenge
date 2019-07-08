import { ActivatedRoute } from '@angular/router';
import { LogService } from './../services/log.service';
import { Log } from './../services/log';
import { Component, OnInit } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { NotifierService } from 'angular-notifier';
import { async } from '@angular/core/testing';

@Component({
  selector: 'app-lista-log',
  templateUrl: './lista-log.component.html',
  styleUrls: ['./lista-log.component.css']
})
export class ListaLogComponent implements OnInit {

  log: Log[] = [];
  public paginaAtual = 1;

  constructor(
    private logService: LogService,
    private activatedRoute: ActivatedRoute,private spinner:NgxSpinnerService,
    notifier: NotifierService
  ) {
    this.notifier = notifier;
   }


   ngAfterViewInit() {
  
     /* this.spinner.show();
      this.logService.listAll().subscribe(log =>  this.log =  log);
      this.spinner.hide();*/

     
  
}

 async ngOnInit() {
  this.spinner.show();
  this.log = await this.logService.listAll();
  this.spinner.hide();
  
  }

  model: any = {};
  private notifier: NotifierService;

async excluirLog(id:Number){
    this.spinner.show();
   await this.logService.excluirLog(id);

   this.notifier.notify('success','Excluído  com Sucesso!');
   this.log = await this.logService.listAll();
   this.spinner.hide();

  }

}
