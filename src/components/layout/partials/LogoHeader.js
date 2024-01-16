import React from 'react';
import classNames from 'classnames';
import { Link } from 'react-router-dom';
import Image from '../../elements/Image';

const LogoHeader = ({
  className,
  ...props
}) => {

  const classes = classNames(
    'brand',
    className
  );

  return (
    <div
      {...props}
      className={classes}
    >
      <h1 className="m-0">
        <a href="http://localhost:8000">
          <Image
            src={require('./../../../assets/images/bitcoin3.jpg')}
            alt="Open"
            width={200}
            height={32} />
        </a>
      </h1>
    </div>
  );
}

export default LogoHeader;