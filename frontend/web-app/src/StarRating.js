import React, { useState, useEffect, memo } from "react";

const StarRating = memo(({ songId, onChange, initialRating }) => {
  const [rating, setRating] = useState(initialRating);

  useEffect(() => {
    setRating(initialRating);
  }, [initialRating]);

  const handleClick = (value) => {
    setRating(value);
    onChange(value, songId);
  };

  return (
    <div>
      {[1, 2, 3, 4, 5].map((star) => (
        <span
          key={star}
          className={`star ${star <= rating ? "on" : "off"}`}
          onClick={() => handleClick(star)}
          style={{ cursor: "pointer", color: star <= rating ? "gold" : "grey" }}
        >
          &#9733;
        </span>
      ))}
    </div>
  );
});

export default StarRating;
