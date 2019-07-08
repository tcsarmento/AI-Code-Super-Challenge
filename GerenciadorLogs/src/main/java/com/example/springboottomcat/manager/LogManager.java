package com.example.springboottomcat.manager;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.example.springboottomcat.modelo.Log;
import com.example.springboottomcat.repository.LogRepository;

@Component
public class LogManager {
	
	@Autowired
	private LogRepository logRepository;
	
	private SimpleDateFormat dataFormatada =new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");  
	  
	
	@PersistenceContext
	private EntityManager em;
	@Transactional
	public Log salvarLogManual(Log log) throws Exception {
		try {
			if(log.getArquivo() != null)
				salvarLogBatch(log.getArquivo());
			logRepository.save(log);
		}catch (Exception e) {
			throw e;
		}
		
		return log;
	}
	
	int count = 1;
	@Transactional
	public Log salvarLogBatch(Log log) {
		try {
			
			em.persist(log);
			
			if (count % 50000 == 0) {
	            em.flush();
	            em.clear();
		    }
			
			count++;
			
		}catch (Exception e) {
			throw e;
		}
		
		return log;
	}
	
	@Transactional
	public Log salvarLogBatch(String arquivoBase64) throws Exception {
		try {
			
			byte[] content = Base64.getDecoder().decode(arquivoBase64);
	        InputStream is = null;
	        BufferedReader bfReader = null;
	        try {
	            is = new ByteArrayInputStream(content);
	            bfReader = new BufferedReader(new InputStreamReader(is));
	            String temp = null;
	         
	            while((temp = bfReader.readLine()) != null){
	            	count++;
	            	
	            	String[] dados = temp.split("\\|");
	              
	            	salvarLogBatch(new Log(dataFormatada.parse(dados[0]),dados[1],dados[2], dados[3], dados[4]));
	            	
	               // System.out.println(temp);
	            }
	        } catch (IOException e) {
	            e.printStackTrace();
	        } finally {
	            try{
	                if(is != null) is.close();
	            } catch (Exception ex){
	                 
	            }
	        }
			
			return null;
			
		}catch (Exception e) {
			throw e;
		}
	}
	
	public List<Log> buscarTodosLog() {
		try {
			return logRepository.findAll();
		}catch (Exception e) {
			throw e;
		}
	}
	
	public Log buscarPorIdLog(Integer  id) {
		try {
			return logRepository.findOne(id);
		}catch (Exception e) {
			throw e;
		}
	}
	
	public void deletarPorIdLog(Integer  id) {
		try {
			 logRepository.delete(buscarPorIdLog(id));
		}catch (Exception e) {
			throw e;
		}
	}
}
