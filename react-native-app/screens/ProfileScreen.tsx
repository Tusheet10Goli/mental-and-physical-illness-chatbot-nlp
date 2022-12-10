
import { StyleSheet, TouchableOpacity, Image, TextInput} from 'react-native';
import React, {useState, useEffect} from 'react'

import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { RootAppTabScreenProps } from '../types';
import axios from 'axios';
import { useFocusEffect } from '@react-navigation/native';

export default function ProfileScreen({ route, navigation }: RootAppTabScreenProps<'Profile'>) {

  // const emailId = route.params.email
  // console.log(emailId)

  const baseUrl = 'http://10.0.2.2:5000'
  

  const [fName, setFName] = useState('');
  const [mName, setMName] = useState('');
  const [lName, setLName] = useState('');
  const [fullName, setFullName] = useState('');
  const [dob, setDOB] = useState('');
  const [gender, setGender] = useState('');
  const [email, setEmail] = useState('');

  useFocusEffect(
    React.useCallback(() => {
      axios.get(baseUrl + '/get-user-data')
      .then((response) => {
        var data = response.data["RESPONSE"]
        console.log(data)
        setFName(data[1])
        setMName(data[2])
        setLName(data[3])
        setDOB(data[4])
        setGender(data[5])
        setEmail(data[6])

        setFullName(fName + ' ' + mName + ' ' + lName)
      
      

      }, (error) => {
        console.log(error);
        console.log('network error')
      });
        
        
    }, [])
  );

  function trueGender(i) {
    if (i === 'M')
      return 'Male'
    else if (i === 'F')
      return 'Female'
    else 
      return ''
  }

    

  return (
    <View style={styles.container}>
    <View style={styles.container2}>
      
      {/* <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" /> */}
      
      <Image source = {require("../assets/images/mentalhealthlogo.png")} 
      style={styles.image}
      resizeMode={'contain'}
      />

      <Text style={styles.name}>{fName} {mName} {lName}</Text>
      
      <Text style={styles.dob}>Date of Birth: {dob}</Text>

      <Text style={styles.gender}>Gender: {trueGender(gender)}</Text>

      <Text style={styles.email}>Email: {email}</Text>

      {/* <TouchableOpacity style={styles.editBtn} >
        <Text style={{color:'black'}}>Edit Profile</Text>
      </TouchableOpacity> */}
      
      <TouchableOpacity style={styles.logoutBtn} onPress={() => navigation.navigate('Root')}>
        <Text style={{color:'white'}}>LOGOUT</Text>
      </TouchableOpacity>

    
    </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center'
    
  },
  container2: {
    
    padding: 20,
    width: 380,
    height: 640,
    borderRadius: 30,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    alignItems: 'center',
  },
  image : {
    marginTop: 30,
    marginBottom: 20,
    width: 175, 
    height: 175
  },
  title: {
    
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 40,
  },
  name: {
    
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 40,
  },
  dob: { 
    fontSize: 17,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  gender: {
    fontSize: 17,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  email: {
    fontSize: 17,
    fontWeight: 'bold',
    marginBottom: 30,
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
  editBtn: {
    width:"40%",
    borderRadius:25,
    height:45,
    alignItems:"center",
    justifyContent:"center",
    marginTop:30,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    backgroundColor: 'white'
  },
  logoutBtn: {
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
  }
});