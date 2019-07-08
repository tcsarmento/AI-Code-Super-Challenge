import { async } from '@angular/core/testing';
import { Log } from './log';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { error } from '@angular/compiler/src/util';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';


@Injectable({ providedIn: 'root' })
export class LogService {
    httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'DELETE, POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With'
        })
    };
    constructor(private http: HttpClient){}
    log: Log[] = [];

    async listAll(){
      // return await this.http.get<Log[]>(environment.host + '/buscar-todos-log');
       return await this.http.get<Log[]>(environment.host + '/buscar-todos-log').toPromise();
    }

    findById(id: any): Observable<any>{
        return this.http.get<any[]>(environment.host + '/buscar-id-log/'+id);
    }

    salvarLog(Log: any): Observable<any>{
        return this.http.post<any>(environment.host + '/salvar-log-manual', Log, this.httpOptions);
    }

    async excluirLog(id: any){
        return await this.http.get<any[]>(environment.host + '/deletar-id-log/'+id).toPromise();
    }
}