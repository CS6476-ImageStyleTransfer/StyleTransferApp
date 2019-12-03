import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub  } from '@fortawesome/fontawesome-free-brands'

export default () => (
  <footer>
    <a 
      href='https://github.com/CS6476-ImageStyleTransfer/StyleTransferApp' 
      title='Github repo'
      target='_blank'
      rel='noopener noreferrer'
      className={'small-button github'}
    >
      <FontAwesomeIcon icon={faGithub} size='3x' color='#fff' />
    </a>
  </footer>
)