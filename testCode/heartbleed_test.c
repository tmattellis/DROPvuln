int dtlsl_process_heartbeat(SSL *s)
{
	unsigned char *p = &s->s3->rrec.data[0], *pl;
	unsigned short hbtype;
	unsigned int payload;
	unsigned int padding = 16;
	
	hbtype = *p++;
	n2s(p, payload);
	
	if(1 + 2 + payload + 16 > s->s3->rrec.length){
		return 0;
	}

	p1 = p;
	
	if (hbtype == TLS1_HB_REQUEST) {
		unsigned char *buffer, *bp;
		int r;
		// ...
		buffer = OPENSSL_malloc(1+2+payload+padding);
		bp = buffer;
		
		*bp++ = TLS1_HB_RESPONSE;
		s2n(payload,bp);
		memcpy(bp,p1,payload);
		bp += payload;
		
		RAND_pseudo_bytes(bp,padding);
		r = dtlsl_write_bytes(s,TLS1_RT_HEARTBEAT,buffer,3+payload+padding);
		
		if(r<0) { return r;}
	}

	return 0;
}
