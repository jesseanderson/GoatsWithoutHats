package com.hackcmu.goatswithouthats;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;

import android.content.Intent;
import android.os.Message;
import android.util.Log;

public class Connection extends Thread {
	
	public Socket s;
	String hostname;
	int port;
	InputStream instream;
	OutputStream outstream;
	ArrayList<Byte> output = new ArrayList<Byte>();
	boolean connected = false;
	Connectable parent;

	public Connection(String hostname, int port, Connectable parent)
	{
		this.hostname = hostname;
		this.port = port;
		this.parent = parent;
	}
	
	public void run()
	{
		try
		{
			s = new Socket(hostname, port);
			instream = s.getInputStream();
			outstream = s.getOutputStream();
		}
		catch (UnknownHostException e)
		{
			fail();
			return;
		}
		catch (IOException e)
		{
			fail();
			return;
		}
		connected = true;
		success();
		byte[] buffer = new byte[1024];
		int bytes;
		while(true)
		{
			try
			{
				bytes = instream.read(buffer);
				for(int i=0; i<bytes; i++)
				{
					output.add(buffer[i]);
				}
			}
			catch(IOException e)
			{
				fail();
				return;
			}
		}
	}
	
	public void pushByte(byte b)
	{
		try
		{
			byte[] buffer = {b};
			outstream.write(buffer);
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}
	
	private void fail()
	{
		parent.getHandler().sendEmptyMessage(1);
	}
	
	private void success()
	{
		parent.getHandler().sendEmptyMessage(2);
	}
	
}
