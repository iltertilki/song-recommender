import React, { useState, useEffect, memo } from "react";
const StarRating = memo(({ songId, onChange, initialRating }) => {
  const [rating, setRating] = useState(initialRating);

  useEffect(() => {
    console.log("Initial Rating updated:", initialRating);
    setRating(initialRating);
  }, [initialRating]);

  const handleClick = (value) => {
    setRating(value);
    onChange(value, songId);
  };

  return (
    <div>
      {[1, 2, 3, 4, 5].map((star, index) => (
        <span
          key={index}
          role="button"
          aria-label={`Rate ${star} stars`}
          className={`star ${star <= rating ? "on" : "off"}`}
          onClick={() => handleClick(star)}
          style={{ cursor: "pointer" }} // Ensure it's clear this is clickable
        >
          &#9733;
        </span>
      ))}
    </div>
  );
});

export default StarRating;
