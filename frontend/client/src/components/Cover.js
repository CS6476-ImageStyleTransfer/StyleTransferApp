import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faImage } from '@fortawesome/free-solid-svg-icons'

export default (props) => 
  <div className='cover-wrapper'>
    <div className='cover'>
      <label>
        <FontAwesomeIcon icon={faImage} color='#3B5998' size='10x' />
      </label>
    </div>
  </div>