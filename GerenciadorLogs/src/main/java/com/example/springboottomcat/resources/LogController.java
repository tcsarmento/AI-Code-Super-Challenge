package com.example.springboottomcat.resources;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.springboottomcat.manager.LogManager;
import com.example.springboottomcat.modelo.Log;

@RestController
@RequestMapping("/log")
@CrossOrigin(origins = "http://localhost:4200")
public class LogController {
	
	@Autowired
	private LogManager logManager;
	
	@PostMapping(produces= "application/json")
	@RequestMapping("/editar-log-manual")
	public Log editarLogManual(@RequestBody Log log) throws Exception{
		
		return logManager.salvarLogManual(log);
	}
	
	@PostMapping(produces= "application/json")
	@RequestMapping("/salvar-log-manual")
	public Log salvarLogManual(@RequestBody Log log) throws Exception{
		if(log.getArquivo() != null) log.setArquivo(log.getArquivo().replaceAll("data:application/octet-stream;base64,", ""));
		return logManager.salvarLogManual(log);
	}
	
	@GetMapping(produces= "application/json")
	@RequestMapping("/buscar-todos-log")
	public List<Log> buscarTodosLog(){
		
		return logManager.buscarTodosLog();
	}
	
	@GetMapping(produces= "application/json")
	@RequestMapping("/buscar-id-log/{id}")
	public Log buscarPorIdLog(@PathVariable Integer id){
		
		return logManager.buscarPorIdLog(id);
	}
	
	@GetMapping(produces= "application/json")
	@RequestMapping("/deletar-id-log/{id}")
	public Integer deletarPorIdLog(@PathVariable Integer id){
		
		 logManager.deletarPorIdLog(id);
		 
		 return id;
	}
	
	@PostMapping(produces= "application/json")
	@RequestMapping("/inserir-log-batch")
	public void inserirLogBatch(@RequestBody String arquivoBase64) throws Exception{
		
		 logManager.salvarLogBatch(arquivoBase64);
	}
	
	
}
