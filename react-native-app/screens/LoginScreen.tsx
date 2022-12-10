import { StyleSheet, TouchableOpacity, Image, TextInput} from 'react-native';
import React, {useState} from 'react'

import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { RootTabScreenProps } from '../types';
import axios from 'axios';
import { useEffect } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import { LogBox, Button } from 'react-native';


export default function LoginScreen({ navigation }: RootTabScreenProps<'Login'>) {

  LogBox.ignoreLogs(['Warning: ...']); // Ignore log notification by message
  LogBox.ignoreAllLogs();//Ignore all log notifications

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errMsg, setErrMsg] = useState('')


  const baseUrl = 'http://10.0.2.2:5000'

  useFocusEffect(
    React.useCallback(() => {
            
            
        // setEmail('')
        // setPassword('')
        setErrMsg('')
    }, [])
    
  );


  const loginCall = async ()=> { 
    axios.get(baseUrl + '/authenticate-user/' + email + '/' + password)
    .then((response) => {
      if (response.data['MESSAGE'] === 'User Logged In!') {
        
        navigation.navigate('RootApp', {
          email: email
        })
      } else {
        console.log('yes')
        setErrMsg('Invalid username/password. Please try logging in again.')
      }
    }, (error) => {
      console.log(error);
      console.log('no')
      setErrMsg('Invalid username/password. Please try logging in again.')
    });
}
  


  return (
    <View style={styles.container}>
      
      
      <Image source = {require("../assets/images/mentalhealthlogo.png")} 
      style={styles.image}
      resizeMode={'contain'}
      />
      <Text style={styles.title}>
          Mental and Physical Illness (MAPI) Chatbot
      </Text>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Email."
          placeholderTextColor="#003f5c"
          onChangeText={(email) => setEmail(email)}
        />
      </View>
 
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Password."
          placeholderTextColor="#003f5c"
          secureTextEntry={true}
          onChangeText={(password) => setPassword(password)}
        />
      </View>
      
      <TouchableOpacity>
        <Text style={styles.forgot_button}>Forgot Password?</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.loginBtn} onPress={() => 
        // navigation.navigate('RootApp')
        loginCall()
      }>
        <Text style={{color:'white'}}>LOGIN</Text>
      </TouchableOpacity>

      <Text style={styles.errMsg}>
          {errMsg}
      </Text>
      
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  image : {
    marginBottom: 20,
    width: 125, 
    height: 125
  },
  inputView: {
    borderRadius: 30,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "70%",
    height: 45,
    marginBottom: 20,
    alignItems: "center",
  },
  TextInput: {
    height: 50,
    flex: 1,
    padding: 10,
    marginLeft: 20,
  },
  title: {
    width: 300,
    textAlign: 'center',
    // alignItems: 'center',
    // justifyContent: 'center',
    marginBottom: 40,
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
  forgot_button: {
    height: 30,
    marginBottom: 30,
  }, 
  loginBtn: {
   width:"40%",
   borderRadius:25,
   height:45,
   alignItems:"center",
   justifyContent:"center",
   marginTop:30,
  //  borderWidth: 2, 
  //  borderColor: 'purple',  
  //  borderStyle:'solid',
   backgroundColor: '#9932cc'
 },
 errMsg: {
   marginTop: 40,
   color: 'red',
   fontSize: 12
 }
});
