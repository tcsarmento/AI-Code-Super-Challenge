import { LogService } from './../services/log.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Log } from './../services/log';
import { NotifierService } from 'angular-notifier';
import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-form-log',
  templateUrl: './form-log.component.html',
  styleUrls: ['./form-log.component.css']
})
export class FormLogComponent implements OnInit {

  model: any = {};
  private notifier: NotifierService;
  log: Log;
  fileToUpload: File = null;
  arquivoBase64;

  constructor( private activatedRoute: ActivatedRoute,
               private logService: LogService,
               notifier: NotifierService,
               private router: Router,
               private spinner: NgxSpinnerService) { 
    
        this.notifier = notifier;
  }

  ngOnInit(): void {
    this.spinner.show();
    
    this.model = {};
      if(this.activatedRoute.snapshot.params.id){
        const id: number = this.activatedRoute.snapshot.params.id;
        this.logService.findById(id)
                          .subscribe(r =>{
                              this.log = r;
                           
                              this.model = this.log;
                              var datePipe = new DatePipe('en-US'); 
                              var newDate = new Date(this.parseDate(this.model.data));
                              this.model.data = datePipe.transform(newDate, 'yyyy-MM-dd');
        });
      }
          window['xvm']=this;

          this.spinner.hide();
  }

  salvar(){

    if(this.model.data == null){
      this.notifier.notify('warning','O campo data deve ser informado');
      return;
    }
   

    if(this.model.request == null){
      this.notifier.notify('warning','O campo request deve ser informado');
      return;
    }

    if(this.model.userAgent == null){
      this.notifier.notify('warning','O campo User Agent deve ser informado');
      return;
    }

    if(this.model.ip == null){
      this.notifier.notify('warning','O campo IP deve ser informado');
      return;
    }

    this.spinner.show();

    var datePipe = new DatePipe('en-US');
    this.model.data = datePipe.transform(this.model.data, 'yyyy-MM-dd HH:mm:ss');
  
      this.logService.salvarLog(this.model).subscribe(r => {
        
        this.spinner.hide();
     
          this.notifier.notify('success','Cadastro Realizado com Sucesso!');
          this.model = '';
          this.router.navigate(['lista-log']);

          
      
        
      });
  }

changeListener($event) : void {
  this.readThis($event.target);
}

readThis(inputValue: any): void {
  var file:File = inputValue.files[0];
  var myReader:FileReader = new FileReader();

  myReader.onloadend = (e) => {
    this.arquivoBase64 = myReader.result;
    this.model.arquivo = this.arquivoBase64;
    
  }
  myReader.readAsDataURL(file);
}

parseDate(value: any): Date | null {
  if ((typeof value === 'string') && (value.indexOf('/') > -1)) {
    const str = value.split('/');

    const year = Number(str[2]);
    const month = Number(str[1]) - 1;
    const date = Number(str[0]);

    return new Date(year, month, date);
  } else if((typeof value === 'string') && value === '') {
    return new Date();
  }
  const timestamp = typeof value === 'number' ? value : Date.parse(value);
  return isNaN(timestamp) ? null : new Date(timestamp);
}

}
