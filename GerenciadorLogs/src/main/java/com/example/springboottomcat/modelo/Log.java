package com.example.springboottomcat.modelo;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;
import javax.persistence.Transient;

import com.fasterxml.jackson.annotation.JsonFormat;

@Entity
public class Log {

	@Id
    @Column(name="ID", unique=true, nullable=false)
	@SequenceGenerator(name = "ATIVIDADE_ID_GENERATOR", sequenceName = "SQ_ATIVIDADE", initialValue = 1, allocationSize = 1)
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ATIVIDADE_ID_GENERATOR")
    private Integer id;
	
	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
	@Column(name = "DATA")
	private Date data;
	
	@Column(name = "REQUEST")
	private String request;
	
	@Column(name = "STATUS")
	private String status;
	
	@Column(name = "USER_AGENT")
	private String userAgent;
	
	@Column(name = "IP")
	private String ip;
	
	@Transient
	private String arquivo;
	
    public Log() {
	}    

	public Log(Integer id, Date data, String request, String status, String userAgent) {
		super();
		this.id = id;
		this.data = data;
		this.request = request;
		this.status = status;
		this.userAgent = userAgent;
	}
	
	public Log(Date data,String ip,String request, String status, String userAgent) {
		super();
		this.data = data;
		this.ip = ip;
		this.request = request;
		this.status = status;
		this.userAgent = userAgent;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public Date getData() {
		return data;
	}

	public void setData(Date data) {
		this.data = data;
	}

	public String getRequest() {
		return request;
	}

	public void setRequest(String request) {
		this.request = request;
	}

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public String getUserAgent() {
		return userAgent;
	}

	public void setUserAgent(String userAgent) {
		this.userAgent = userAgent;
	}

	public String getArquivo() {
		return arquivo;
	}

	public String getIp() {
		return ip;
	}

	public void setIp(String ip) {
		this.ip = ip;
	}

	public void setArquivo(String arquivo) {
		this.arquivo = arquivo;
	}

	private boolean equalKeys(Object other) {
        if (this==other) {
            return true;
        }
        if (!(other instanceof Log)) {
            return false;
        }
        Log that = (Log) other;
        Object myId = this.getId();
        Object yourId = that.getId();
        if (myId==null ? yourId!=null : !myId.equals(yourId)) {
            return false;
        }
        return true;
    }
	
	@Override
    public boolean equals(Object other) {
        if (!(other instanceof Log)) return false;
        return this.equalKeys(other) && ((Log)other).equalKeys(this);
    }

    @Override
    public int hashCode() {
        int i;
        int result = 17;
        if (getId() == null) {
            i = 0;
        } else {
            i = getId().hashCode();
        }
        result = 37*result + i;
        return result;
    }
}
