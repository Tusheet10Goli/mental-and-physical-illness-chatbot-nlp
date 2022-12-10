/**
 * Learn more about deep linking with React Navigation
 * https://reactnavigation.org/docs/deep-linking
 * https://reactnavigation.org/docs/configuring-links
 */

import { LinkingOptions } from '@react-navigation/native';
import * as Linking from 'expo-linking';

import { RootStackParamList } from '../types';

const linking: LinkingOptions<RootStackParamList> = {
  prefixes: [Linking.makeUrl('/')],
  config: {
    screens: {
      Root: {
        screens: {
          About: {
            screens: {
              AboutScreen: 'one',
            },
          },
          Login: {
            screens: {
              LoginScreen: 'two',
            },
          },
          Register: {
            screens: {
              RegisterScreen: 'three',
            },
          },
        },
      },
      RootApp: {
        screens: {
          Profile: {
            screens: {
              ProfileScreen: 'one',
            },
          },
          About: {
            screens: {
              AboutScreen2: 'two',
            },
          },
          Chat: {
            screens: {
              ChatScreen: 'three',
            },
          },
        },
      },
      NotFound: '*',
    },
  },
};

export default linking;
