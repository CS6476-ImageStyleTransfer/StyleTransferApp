import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faServer } from '@fortawesome/free-solid-svg-icons'

export default () => 
  <div className='loading-wrapper fadein'>
    <h4>Please start the image upload server...</h4>
    <div className='loading'>
      <div className='background'>
        <div className='icon'>
          <FontAwesomeIcon icon={faServer} size='5x' color='#006633' />
        </div>
      </div>
    </div>
  </div>