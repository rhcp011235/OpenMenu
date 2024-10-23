<?php

// This is the original open menu PHP source that is actually used to FMI off the device

	function fmipWipeToken($appleID, $Password)
	{
		$url = 'https://setup.icloud.com/setup/fmipauthenticate/$APPLE_ID$';
	    $post_data = '{
		  "clientContext": {
			"productType": "iPhone6,1",
			"buildVersion": "376",
			"appName": "FindMyiPhone",
			"osVersion": "7.1.2",
			"appVersion": "3.0",
			"clientTimestamp": 507669952542,
			"inactiveTime": 1,
			"deviceUDID": "67bbe2ad90e7106f462cb15df7a49e0bb2a8fiio"
		  },
		  "serverContext": {}
		}';
		$bacio=base64_encode($appleID.':'.$Password);
		$ch = curl_init(); 
		curl_setopt($ch, CURLOPT_URL , $url ); 
		curl_setopt($ch, CURLOPT_RETURNTRANSFER , 1); 
		curl_setopt($ch, CURLOPT_TIMEOUT , 60); 
		curl_setopt($ch, CURLOPT_VERBOSE, 0);
        curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_HTTPHEADER, 
			array(
				"Host: setup.icloud.com", "Accept: */*",  
				"Authorization: Basic".$bacio, 
				"Proxy-Connection: keep-alive", 
				"X-MMe-Country: EC", "X-MMe-Client-Info: <iPhone7,2> <iPhone OS;8.1.2;12B440> <com.apple.AppleAccount/1.0 (com.apple.Preferences/1.0)>", 
				"Accept-Language: es-es", 
				"Content-Type: text/plist", 
				"Connection: keep-alive"
			)
		);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
		curl_setopt($ch, CURLOPT_USERAGENT , "User-Agent: Ajustes/1.0 CFNetwork/711.1.16 Darwin/14.0.0" );
		curl_setopt($ch, CURLOPT_POST , 1); 
		curl_setopt($ch, CURLOPT_POSTFIELDS , $post_data ); 
		$xml_response = curl_exec($ch); 
 
		if (curl_errno($ch)) { 
			$error_message = curl_error($ch); 
			$error_no = curl_errno($ch);
			echo "error_message: " . $error_message . "<br>";
			echo "error_no: " . $error_no . "<br>";
		}
 
		curl_close($ch);
 
		$response = $xml_response;
		echo $response; 
		$DSID = explode("<key>dsid</key>", $response)[1];
		$DSID = explode("<string>", $DSID)[1];
		$DSID = explode("</string>", $DSID)[0];
		$WPT = explode("<key>mmeFMIPWipeToken</key>", $response)[1];
		$WPT = explode("<string>", $WPT)[1];
		$WPT = explode("</string>", $WPT)[0];
		
		return array("dsid" => $DSID, "wipeToken" => $WPT);

	}


	function remove($dsid, $udid, $SerialNumber, $mmeFMIPWipeToken, $ProductType)
	{
		$url = "https://p33-fmip.icloud.com/fmipservice/findme/".$dsid."/".$udid."/unregisterV2";
		$post_data = '{
			"serialNumber": "'.$SerialNumber.'",
			"deviceContext": {
				"deviceTS": "2017-02-01T20:33:11.880Z"
			},
			"deviceInfo": {
				"productType": "'.$ProductType.'",
				"udid": "'.$udid.'",
				"fmipDisableReason": 1,
				"buildVersion": "13G36",
				"productVersion": "9.3.5"
			}
		}';
		$bacio=base64_encode($dsid.':'.$mmeFMIPWipeToken);
		$ch = curl_init(); 
		curl_setopt($ch, CURLOPT_URL , $url ); 
		curl_setopt($ch, CURLOPT_RETURNTRANSFER , 1); 
		curl_setopt($ch, CURLOPT_TIMEOUT , 60); 
		curl_setopt($ch, CURLOPT_VERBOSE, 0);
		curl_setopt($ch, CURLOPT_HEADER, 1);
		curl_setopt($ch, CURLOPT_HTTPHEADER, 
			array(
				"Host: p33-fmip.icloud.com", 
				"Accept-Language: es-es", 
				"X-Apple-PrsId: ".$dsid,  
				"Accept: */*",  
				"Content-Type: application/json", 
				"X-Apple-Find-API-Ver: 6.0", 
				"X-Apple-I-MD-RINFO: 17106176", 
				"Connection: keep-alive", 
				"Authorization: Basic ".$bacio, 
				"Content-Length: ".strlen($post_data), 
				"X-Apple-Realm-Support: 1.0"
			)
		);

		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
		curl_setopt($ch, CURLOPT_USERAGENT , "User-Agent: FMDClient/6.0 iPod5,1/13G36" );
		curl_setopt($ch, CURLOPT_POST , 1); 
		curl_setopt($ch, CURLOPT_POSTFIELDS , $post_data );
		$xml_response = curl_exec($ch); 

		if (curl_errno($ch)) { 
			$error_message = curl_error($ch); 
			$error_no = curl_errno($ch);

			echo "error_message: " . $error_message . "<br>";
			echo "error_no: " . $error_no . "<br>";
		}

		curl_close($ch);
		$response = $xml_response;

		return $response;
	}
	
	if(isset($_GET['request'])){
		$Credentials['appleID'] = $_GET['appleID'];
		$Credentials['password'] = $_GET['password'];
		$Credentials['serialNu'] = $_GET['serialNumber'];
		$Credentials['UniqueID'] = $_GET['udid'];
		$Credentials['product'] = $_GET['pt'];
		$wipeInfo = fmipWipeToken($Credentials['appleID'], $Credentials['password']);
		$dsid = $wipeInfo["dsid"];
		$mmeFMIPWipeToken = $wipeInfo["wipeToken"];
		echo remove($dsid, $Credentials['UniqueID'], $Credentials['serialNu'], $mmeFMIPWipeToken, $Credentials['product']);
	}
?>