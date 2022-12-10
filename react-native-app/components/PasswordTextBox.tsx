
import React from 'react';
import { Item, Input, Icon, Label } from 'native-base';

//This code has to do with the password fields on the Login and Create Account screens
class PasswordTextBox extends React.Component {
    state = {
        icon: "eye-off",
        password: true
    };

    _changeIcon() {
        this.setState(prevState => ({
            icon: prevState.icon === 'eye' ? 'eye-off' : 'eye',
            password: !prevState.password
        }));
    }

    render() {
        const { label, icon, onChange } = this.props;
        return (
            <Item floatingLabel>
                <Icon
                    active name={icon}
                />
                <Label style={{ color: "white" }}>Password</Label>
                <Input
                    secureTextEntry={this.state.password}
                    onChangeText={(e) => onChange(e)}
                    maxLength={160}
                />
                <Icon
                    name={this.state.icon}
                    onPress={() => this._changeIcon()}
                />
            </Item>
        );
    }
}
export default PasswordTextBox;