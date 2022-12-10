import { StyleSheet, TouchableOpacity, Image, TextInput, ScrollView} from 'react-native';
import React, {useState} from 'react'

import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import axios from 'axios';
import {Dropdown } from 'react-native-material-dropdown-v2-fixed';
import { LogBox, Button } from 'react-native';
import DateTimePickerModal from "react-native-modal-datetime-picker";


export default function RegisterScreen() {

  LogBox.ignoreLogs(['Warning: ...']); // Ignore log notification by message
  LogBox.ignoreAllLogs();//Ignore all log notifications

  


  const baseUrl = 'http://10.0.2.2:5000'

  const [fName, setFName] = useState('');
  const [mName, setMName] = useState('');
  const [lName, setLName] = useState('');
  const [dob, setDOB] = useState(new Date());
  const [gender, setGender] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  

  const [isDatePickerVisible, setDatePickerVisibility] = useState(false);

  const showDatePicker = () => {
    setDatePickerVisibility(true);
  };

  const hideDatePicker = () => {
    setDatePickerVisibility(false);
  };

  //handles the user selecting a date for date of birth
  const handleConfirm = (date) => {
    var pickedDate = dob;
    const currentDate = date || pickedDate;
    hideDatePicker();
    setDOB(date);
  };

  const [errMsg, setErrMsg] = useState('')

  let genderData = [{
    label: 'Male',
    value: 'M'
  },
  {
    label: 'Female',
    value: 'F'
  }]


  const registerCall = async(obj) => {
      axios.post(baseUrl + '/register-user', obj)
      .then((response) => {
        console.log(response);
        setErrMsg('User is Registered!')
      }, (error) => {
        console.log(error);
        setErrMsg('There is an error with registration.')
      });
    };

  function submit() {
    const obj = {
      fname: fName,
      mname: mName,
      lname: lName,
      dob: dob.toISOString().split('T')[0],
      gender: gender, 
      email: email,
      password: password
    }
    console.log(obj)

    registerCall(obj)



  }

  function displayDate() {
    return dob.toISOString().split('T')[0]
  }

  return (
    <ScrollView style={styles.scrollContainer}>
    <View style={styles.container}>

    
      <Text style={styles.title}>
          Register
      </Text>
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="First Name"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setFName(text)}
        />
      </View>
 
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Middle Name"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setMName(text)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Last Name"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setLName(text)}
        />
      </View>

      {/* <View style={styles.inputView3}>
        <TouchableOpacity style={styles.buttonView} onPress = {showDatePicker}>
            <Text style={{color:'#9932cc'}}>Show Date Picker</Text>
        </TouchableOpacity>
        <DateTimePickerModal
          isVisible={isDatePickerVisible}
          mode="date"
          onConfirm={(text) => setDOB(text.toString().slice(0, text.toString().indexOf('T')))}
          onCancel={hideDatePicker}
        />
      </View> */}

      <View style={styles.inputView}>
        {/* <TextInput
          style={styles.TextInput}
          placeholder="Date of Birth"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setDOB(text)}
        /> */}
        {/* <View style={{alignItems: 'baseline'}}> */}
        <Text style={{marginTop:10, marginLeft:20,}}>{displayDate()}</Text>
        {/* </View> */}
        <TouchableOpacity style={styles.buttonView} onPress = {showDatePicker}>
            <Text style={{color:'white'}}>Pick Birthdate</Text>
        </TouchableOpacity>
        {/* <Button style={styles.buttonView} onPress={showDatePicker} title="Pick birthdate" /> */}
        <DateTimePickerModal
            isVisible={isDatePickerVisible}
            mode={'date'}
            onConfirm={handleConfirm}
            onCancel={hideDatePicker}
            maximumDate={new Date()}
            minimumDate={new Date(1930, 12, 31)}
            //display={'inline'}
            timeZoneOffsetInMinutes={0}
            date={dob}/>
      </View>

      {/* <View>
      
      </View> */}

      <View style={styles.inputView2}>
        {/* <TextInput
          style={styles.TextInput}
          placeholder="Gender"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setGender(text)}
        /> */}
        <Dropdown 
          style={styles.Dropdown}
          // style={{backgroundColor:'white'}}
          label='Gender'
          data={genderData}
          onChangeText={(text) => setGender(text)}
        
        />

        
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Email Address"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setEmail(text)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Password"
          placeholderTextColor="#003f5c"
          onChangeText={(text) => setPassword(text)}
        />
      </View>

      <TouchableOpacity style={styles.registerBtn} onPress = {() => submit()}>
        <Text style={{color:'white'}}>Submit</Text>
      </TouchableOpacity>

      <Text style={{marginTop: 20}}>{errMsg}</Text>


    </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({

  scrollContainer: {
    backgroundColor: 'white'
  },
  container: {
    flex: 1,
    alignItems: 'center',
    
  },
  inputView: {
    display:'flex',
    borderRadius: 10,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "90%",
    height: 40,
    marginBottom: 20,
    
  },
  inputView2: {
    borderRadius: 10,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "90%",
    height: 60,
    marginBottom: 20,
    alignItems: 'center'
    
  },
  inputView3: {
    borderRadius: 10,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "90%",
    height: 40,
    marginBottom: 20,
    alignItems: 'center'
    
  },
  Dropdown: {
    backgroundColor:'white',
    height: 50,
    width: 350,
    marginTop: 0
    // flex: 1,
    // padding: 5,
    // marginLeft: 0,
  },
  buttonView: {
    backgroundColor:'#9932cc',
    // width:"40%",
    marginLeft: 210,
    borderRadius:25,
    height:35,
    // height: 50,
    width: 150,
    marginTop: -28.5,
    alignItems:"center",
    justifyContent:"center",
    // flex: 1,
    // padding: 5,
    // marginLeft: 0,
  },
  TextInput: {
    height: 50,
    flex: 1,
    padding: 5,
    marginLeft: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 100,
    marginBottom: 40,
  },
  registerBtn: {
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


