package com.hackcmu.goatswithouthats;

import java.io.IOException;

import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

public class NewGameActivity extends Activity implements Connectable{

	public int colorChoice = 0;
	public String hostname = "";
	public Connection c = null;
	int[] distances;
	MediaPlayer[] sounds;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_new_game);
		
		Spinner spinner = (Spinner) findViewById(R.id.colorspinner);
		
		ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
		        R.array.color_array, android.R.layout.simple_spinner_item);
		adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
		
		spinner.setAdapter(adapter);
	}


	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.new_game, menu);
		return true;
    }

    public void onNothingSelected(AdapterView<?> parent)
    {
        return;
    }
    
    public void clickedConnect(View view)
    {
    	EditText e = (EditText) findViewById(R.id.hostnameedittext);
    	hostname = e.getText().toString();
    	c = new Connection(hostname, 50000, this);
    	c.start();
    }
    
    private final Handler handler = new Handler()
    {
    	public void handleMessage(Message msg)
    	{
    		switch(msg.what)
    		{
    		case 0:
    			sound();
    			break;
    		case 1:
    			connectFail();
    			break;
    		case 2:
    			connectSuccess();
    			break;
    		}
    	}
    };
    
    public Handler getHandler(){return handler;}
    
    public void connectFail()
    {
    	TextView tv = (TextView) findViewById(R.id.connecterror);
    	tv.setText(getString(R.string.connect_error));
    	c = null;
    }

    public void connectSuccess()
    {
    	Spinner sp = (Spinner) findViewById(R.id.colorspinner);
    	colorChoice = sp.getSelectedItemPosition();
    	sp.setVisibility(View.INVISIBLE);
    	c.pushByte((byte)colorChoice);
    	View v = findViewById(R.id.connecterror);
    	v.setVisibility(View.INVISIBLE);
    	v = findViewById(R.id.hostnameedittext);
    	v.setVisibility(View.INVISIBLE);
    	v = findViewById(R.id.colortextview);
    	v.setVisibility(View.INVISIBLE);
    	v = findViewById(R.id.servertextview);
    	v.setVisibility(View.INVISIBLE);
    	v = findViewById(R.id.connectbutton);
    	v.setVisibility(View.INVISIBLE);
    	TextView tv = (TextView) findViewById(R.id.findtext);
    	distances = new int[getResources().getInteger(R.integer.num_animals)];
    	sounds = new MediaPlayer[getResources().getInteger(R.integer.num_animals)];
    	int animal = (int)(Math.random()*getResources().getInteger(R.integer.num_animals));
    	switch(animal)
    	{
    	case 0:
    		tv.setText(R.string.find0);
    		break;
    	}
    	for(int i=0; i<sounds.length; i++)
    	{
    		sounds[i] = new MediaPlayer();
    	}
    	tv.setVisibility(View.VISIBLE);
    	sound();
    }
    
    public void sound()
    {
    	processDistances();
    	for(int i=0; i<sounds.length; i++)
    	{
    		if(sounds[i] != null && !soundIsPlaying(sounds[i]))
    		{
    			Log.d("FUCK A GOAT", "DICK");
    			sounds[i].release();
    			int resid = getSoundId(i, distances[i]);
    			sounds[i] = MediaPlayer.create(this, resid);
    			sounds[i].start();
    		}
    		else if(sounds[i] == null)
    		{
    			Log.d("DICKS", "AND DICKS");
    			int resid = getSoundId(i, distances[i]);
    			sounds[i] = MediaPlayer.create(this, resid);
    			sounds[i].start();
    		}
    	}
    	handler.sendEmptyMessageDelayed(0, 200);
    }
    
    public void processDistances()
    {
    	for(Byte b : c.output)
    	{
    		Log.d("PENIS", ""+b);
    		if(b/10 <= distances.length)
    		{
    			distances[b/10]=b%10;
    		}
    	}
    	c.output.clear();
    }
    
    public int getSoundId(int animal, int distance)
    {
    	Log.d("BALLS", animal+" , "+distance);
    	switch(animal)
    	{
    	case 0:
    		switch(distance)
    		{
    		case 0: return R.raw.cow_vol1;
    		case 1: return R.raw.cow_vol2;
    		case 2: return R.raw.cow_vol3;
    		case 3: return R.raw.cow_vol4;
    		case 4: return R.raw.cow_vol5;
    		case 5: return R.raw.cow_vol6;
    		case 6: return R.raw.cow_vol7;
    		case 7: return R.raw.cow_vol8;
    		case 8: return R.raw.cow_vol9;
    		}
    		break;
    	}
    	return 0;
    }
    
    public boolean soundIsPlaying(MediaPlayer mp)
    {
    	try
    	{
    		return mp.isPlaying();
    	}
    	catch(Exception e){}
    	return false;
    }
    
}
