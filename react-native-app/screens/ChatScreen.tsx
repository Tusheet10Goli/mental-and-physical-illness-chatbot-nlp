import React, { useState, useCallback, useEffect} from 'react'
import { GiftedChat, Bubble} from 'react-native-gifted-chat'
import { Text, View } from '../components/Themed';
import { StyleSheet, TouchableOpacity, Image, TextInput, } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import axios from 'axios';
import { BottomTabView } from '@react-navigation/bottom-tabs';
import TypingIndicator from "react-native-gifted-chat/lib/TypingIndicator"
import { setStatusBarNetworkActivityIndicatorVisible } from 'expo-status-bar';


export default function ChatScreen(props) {
  const [messages, setMessages] = useState([]);
  const bigMessages = []
  const [typing, setTyping] = useState(false);

  const baseUrl = 'http://10.0.2.2:5000'

  const BOT = {
    _id: 2,
    name: 'Mr.Bot',
    // avatar: 'https://placeimg.com/140/140/any'
  }



  const sampleCall = async (message1, message2)=> { 
    
      console.log('what!')
      axios.get(baseUrl + '/health-check')
      .then((response) => {
        var txt = response.data["METHOD"];
        sendBotResponse(txt)
        sendBotResponse(message1)
        sendBotResponse(message2)
        console.log(message1 + message2)
        

      }, (error) => {
        console.log(error);
        console.log('network error')
      });
    
  };



  const getResponse = async (message)=> { 
    const obj = {
      message: message
    }
    axios.post(baseUrl + '/send-message', obj)
    .then((response) => {
      var responseText = response.data['RESPONSE'];
      setTyping(false)
      sendBotResponse(responseText.trim())
      console.log(response)
    }, (error) => {
      console.log(error);
    });
};



  useEffect(() => {
    setMessages([
      {
        _id: 2,
        text: 'Please describe your symptoms in one message, and I will diagnose your condition.',
        createdAt: new Date(),
        user: BOT
      },
      {
        _id: 1,
        text: 'Hello, Welcome to the MAPI Chatbot!',
        createdAt: new Date(),
        user: BOT
     },
    ])

    console.log(messages)
  
      
  }, [])


  // useEffect(() => {
  //   sendBotResponse('hey')

  //   // console.log(messages)
  
      
  // }, [messages])


  function sendBotResponse(text) {
    let msg = {
      _id: bigMessages.length + 3,
      text,
      createdAt: new Date(),
      user: BOT
    };

    setMessages(previousMessages => GiftedChat.append(previousMessages, [msg]))
    bigMessages.push(msg)
    

    console.log(messages)
  }

  const onSend = useCallback((messages = [], name, id) => {
    

    setTyping(true)
    
    bigMessages.push(messages)
    setMessages(previousMessages => GiftedChat.append(previousMessages, messages))
    let message = messages[0].text;
    console.log(message)
    console.log(messages)
    // 
    
    // sendBotResponse('hello!')
    getResponse(message)
  }, [])

  function renderBubble(props) {
    return (
      // Step 3: return the component
      <Bubble
        {...props}
        wrapperStyle={{
          right: {
            // Here is the color change
            backgroundColor: '#9932cc'
          }
        }}
        textStyle={{
          right: {
            color: '#fff'
          }
        }}
      />
    );
  }



  const setIsTyping = () => {
    setTyping(!typing)
  }


  const renderFooter = (props) => {
    return <TypingIndicator isTyping={typing}/>
}


  return (
    <View  style={{backgroundColor: 'white',  flex: 1}}>
    <GiftedChat
      messages={messages}
      onSend={messages => onSend(messages, 'John', 1)}
      user={{
        _id: 1,
      }}
      renderBubble={renderBubble}
      renderFooter={renderFooter}
      isTyping={typing}
      
      
    />
    </View>
  )
}
// import { StyleSheet } from 'react-native';

// import EditScreenInfo from '../components/EditScreenInfo';
// import { Text, View } from '../components/Themed';

// export default function ChatScreen() {
//   return (
//     <View style={styles.container}>
//       <Text style={styles.title}>Chat</Text>
//       <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
//       <EditScreenInfo path="/screens/ChatScreen.tsx" />
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     alignItems: 'center',
//     justifyContent: 'center',
//   },
//   title: {
//     fontSize: 20,
//     fontWeight: 'bold',
//   },
//   separator: {
//     marginVertical: 30,
//     height: 1,
//     width: '80%',
//   },
// });