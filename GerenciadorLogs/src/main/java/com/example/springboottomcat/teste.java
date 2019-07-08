package com.example.springboottomcat;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;


public class teste {

	public static void main(String[] args) throws IOException, ParseException {
		/*File file = new File("C:\\access.log");
		byte[] fileContent = FileUtils.readFileToByteArray(file);
		String encodedString = Base64.getEncoder().encodeToString(fileContent);
		
		System.out.println(encodedString);*/
		
		
		  SimpleDateFormat formatter1 =new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");  
		  Date date1=formatter1.parse("2019-01-01 00:00:11.763");  
		  
		  System.out.println(date1);
		
	}
}
